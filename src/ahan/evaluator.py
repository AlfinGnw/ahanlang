import copy
import os
from .ast_nodes import *
from .lexer import Lexer
from .parser import Parser

def _format_value(value):
    if value is None:
        return "kosong"
    if value is True:
        return "dise"
    if value is False:
        return "salah"
    return str(value)


class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        env = self
        while env is not None:
            if name in env.variables:
                return env.variables[name]
            env = env.parent
        raise Exception(f"Variabel '{name}' tidak ditemukan")

    def set(self, name, value):
        env = self
        while env is not None:
            if name in env.variables:
                env.variables[name] = value
                return
            env = env.parent
        self.variables[name] = value

    def define(self, name, value):
        self.variables[name] = value

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class ExitSignal(Exception):
    pass

class Evaluator:
    def __init__(self, main_file=None):
        self.global_env = Environment()
        self._setup_builtins(self.global_env)
        self.current_node = None
        self.main_file = main_file

    def _setup_builtins(self, env):
        # Fungsi output: kaluarken / ahan
        def cetak(*args):
            if len(args) == 0:
                print()
            else:
                val = args[0]
                if val is None:
                    print("kosong")
                else:
                    print(val)
        # Utilitas dict
        def kunci(d):
            if not isinstance(d, dict):
                raise Exception("kunci() memerlukan dictionary")
            return list(d.keys())

        def nilai(d):
            if not isinstance(d, dict):
                raise Exception("nilai() memerlukan dictionary")
            return list(d.values())

        def pasangan(d):
            if not isinstance(d, dict):
                raise Exception("pasangan() memerlukan dictionary")
            return [[k, v] for k, v in d.items()]

        env.define('kunci', kunci)
        env.define('nilai', nilai)
        env.define('pasangan', pasangan)

        # Fungsi input: baco / mitidao
        def baco(*args):
            prompt = ''
            if len(args) > 0:
                prompt = args[0]
            return input(prompt)
        env.define('baco', baco)
        env.define('mitidao', baco)

        # Konversi tipe
        def to_int(value):
            return int(value)
        env.define('int', to_int)

        def to_float(value):
            return float(value)
        env.define('float', to_float)

        def to_str(value):
            return str(value)
        env.define('str', to_str)

        # Panjang list/string
        def panjang(value):
            return len(value)
        env.define('panjang', panjang)

        # Ambil elemen dengan aman: abek(container, index, default=kosong)
        def abek(container, index, default=None):
            try:
                if isinstance(container, (list, str)):
                    if isinstance(index, int):
                        if index < 0:
                            index += len(container)
                        if 0 <= index < len(container):
                            return container[index]
                return default
            except Exception:
                return default
        env.define('abek', abek)

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env
        self.current_node = node

        # Literal
        if isinstance(node, NumberNode):
            return node.value
        if isinstance(node, StringNode):
            return node.value
        if isinstance(node, BooleanNode):
            return node.value
        if isinstance(node, NullNode):
            return None
        if isinstance(node, ListNode):
            return [self.eval(elem, env) for elem in node.elements]
        if isinstance(node, DictNode):
            return {self.eval(k, env): self.eval(v, env) for k, v in node.pairs}

        # Variabel
        if isinstance(node, VariableAccessNode):
            return env.get(node.name)

        # Assignment
        if isinstance(node, AssignmentNode):
            value = self.eval(node.value, env)
            target = node.target

            # Target berupa VariableAccessNode (assignment ke variabel)
            if isinstance(target, VariableAccessNode):
                name = target.name
                if node.op is not None:
                    old_value = env.get(name)
                    value = self._apply_op(old_value, value, node.op)
                env.set(name, value)
                return value

            # Target berupa string (untuk kompatibilitas)
            elif isinstance(target, str):
                if node.op is not None:
                    old_value = env.get(target)
                    value = self._apply_op(old_value, value, node.op)
                env.set(target, value)
                return value

            # Target berupa IndexAccessNode (elemen list atau dict)
            elif isinstance(target, IndexAccessNode):
                target_obj = self.eval(target.target, env)
                index = self.eval(target.index, env)

                if isinstance(target_obj, list):
                    if not isinstance(index, int):
                        raise Exception("Indeks list harus integer")
                    if index < 0:
                        index += len(target_obj)
                    if index < 0 or index >= len(target_obj):
                        raise Exception("Indeks di luar jangkauan")
                    if node.op is not None:
                        old_value = target_obj[index]
                        value = self._apply_op(old_value, value, node.op)
                    target_obj[index] = value
                    return value
                elif isinstance(target_obj, dict):
                    if node.op is not None:
                        if index not in target_obj:
                            raise Exception(f"Kunci '{index}' tidak ada dalam dictionary")
                        old_value = target_obj[index]
                        value = self._apply_op(old_value, value, node.op)
                    target_obj[index] = value
                    return value
                else:
                    raise Exception("Hanya list dan dict yang bisa dimodifikasi elemennya")

        # Operasi biner
        if isinstance(node, BinaryOpNode):
            return self.eval_binary_op(node, env)

        # Unary
        if isinstance(node, UnaryOpNode):
            return self.eval_unary_op(node, env)

        # If
        if isinstance(node, IfNode):
            condition = self.eval(node.condition, env)
            if condition:
                return self.eval_statements(node.body, env)
            else:
                if node.else_body is not None:
                    return self.eval_statements(node.else_body, env)
                else:
                    return None

        # While
        if isinstance(node, WhileNode):
            while self.eval(node.condition, env):
                try:
                    self.eval_statements(node.body, env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
            return None

        # For
        if isinstance(node, ForNode):
            iterable = self.eval(node.iterable, env)
            if not isinstance(iterable, list):
                raise Exception(f"Perulangan 'mek' memerlukan list, ditemukan {type(iterable)}")
            for item in iterable:
                loop_env = Environment(env)
                loop_env.define(node.var_name, item)
                try:
                    self.eval_statements(node.body, loop_env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
            return None

        # Function definition
        if isinstance(node, FunctionDefNode):
            func_copy = copy.copy(node)
            func_copy.closure = env
            env.define(node.name, func_copy)
            return None

        # Return
        if isinstance(node, ReturnNode):
            value = self.eval(node.value, env) if node.value is not None else None
            raise ReturnSignal(value)

        # Slice access
        if isinstance(node, SliceNode):
            return self.eval_slice(node, env)

        # Index access
        if isinstance(node, IndexAccessNode):
            return self.eval_index(node, env)

        # Function call
        if isinstance(node, CallNode):
            return self.eval_call(node, env)

        # PrintNode
        if isinstance(node, PrintNode):
            value = self.eval(node.value, env) if node.value is not None else None
            print(_format_value(value))
            return None

        # InputNode
        if isinstance(node, InputNode):
            prompt = self.eval(node.prompt, env) if node.prompt is not None else ''
            return input(prompt)

        # BlockNode
        if isinstance(node, BlockNode):
            return self.eval_statements(node.statements, env)

        # Exit
        if isinstance(node, ExitNode):
            raise ExitSignal()

        # Show
        if isinstance(node, ShowNode):
            value = self.eval(node.value, env) if node.value is not None else None
            print(_format_value(value), end='')
            return None

        # Import
        if isinstance(node, ImportNode):
            return self.eval_import(node, env)

        # Try/Except
        if isinstance(node, TryNode):
            return self.eval_try(node, env)

        # Break/Continue
        if isinstance(node, BreakNode):
            raise BreakSignal()
        if isinstance(node, ContinueNode):
            raise ContinueSignal()

        raise Exception(f"Node tidak dikenal: {type(node)}")

    def eval_statements(self, statements, env):
        result = None
        for stmt in statements:
            result = self.eval(stmt, env)
        return result

    def eval_binary_op(self, node, env):
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        op = node.op

        if op == 'dan':
            return bool(left) and bool(right)
        if op == 'atau':
            return bool(left) or bool(right)

        if op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise Exception("Pembagian oleh nol")
            return left / right
        if op == '%':
            return left % right
        if op == '^':
            return left ** right

        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return left < right
        if op == '>':
            return left > right
        if op == '<=':
            return left <= right
        if op == '>=':
            return left >= right

        raise Exception(f"Operator tidak dikenal: {op}")

    def eval_unary_op(self, node, env):
        operand = self.eval(node.operand, env)
        if node.op == 'teen':
            return not operand
        if node.op == '-':
            return -operand
        raise Exception(f"Unary operator tidak dikenal: {node.op}")

    def _apply_op(self, left, right, op):
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise Exception("Pembagian oleh nol")
            return left / right
        if op == '%':
            return left % right
        if op == '^':
            return left ** right
        raise Exception(f"Operator tidak dikenal: {op}")

    def eval_index(self, node, env):
        target = self.eval(node.target, env)
        index = self.eval(node.index, env)

        if isinstance(target, list):
            if not isinstance(index, int):
                raise Exception("Indeks list harus integer")
            if index < 0:
                index += len(target)
            if index < 0 or index >= len(target):
                raise Exception("Indeks di luar jangkauan")
            return target[index]
        elif isinstance(target, str):
            if not isinstance(index, int):
                raise Exception("Indeks string harus integer")
            if index < 0:
                index += len(target)
            if index < 0 or index >= len(target):
                raise Exception("Indeks di luar jangkauan")
            return target[index]
        elif isinstance(target, dict):
            if index not in target:
                raise Exception(f"Kunci '{index}' tidak ada dalam dictionary")
            return target[index]
        else:
            raise Exception(f"Tipe {type(target)} tidak mendukung indexing")

    def eval_slice(self, node, env):
        target = self.eval(node.target, env)
        start = self.eval(node.start, env) if node.start is not None else None
        end = self.eval(node.end, env) if node.end is not None else None

        if isinstance(target, list):
            if start is not None and not isinstance(start, int):
                raise Exception("Indeks awal slice harus integer")
            if end is not None and not isinstance(end, int):
                raise Exception("Indeks akhir slice harus integer")
            return target[start:end]
        elif isinstance(target, str):
            if start is not None and not isinstance(start, int):
                raise Exception("Indeks awal slice harus integer")
            if end is not None and not isinstance(end, int):
                raise Exception("Indeks akhir slice harus integer")
            return target[start:end]
        else:
            raise Exception(f"Tipe {type(target)} tidak mendukung slicing")

    def eval_call(self, node, env):
        func_name = node.func_name
        try:
            func = env.get(func_name)
        except Exception:
            raise Exception(f"Fungsi '{func_name}' tidak ditemukan")

        args = [self.eval(arg, env) for arg in node.args]

        if callable(func):
            return func(*args)

        if isinstance(func, FunctionDefNode):
            local_env = Environment(func.closure)
            if len(args) != len(func.params):
                raise Exception(f"Fungsi '{func_name}' memerlukan {len(func.params)} argumen, diberikan {len(args)}")
            for param, arg in zip(func.params, args):
                local_env.define(param, arg)
            try:
                self.eval_statements(func.body, local_env)
                return None
            except ReturnSignal as ret:
                return ret.value

        raise Exception(f"'{func_name}' bukan fungsi yang valid")

    def eval_import(self, node, env):
        filename = node.filename
        if not filename.endswith('.ahan'):
            filename += '.ahan'
        if not os.path.isabs(filename):
            if self.main_file:
                base_dir = os.path.dirname(os.path.abspath(self.main_file))
            else:
                base_dir = os.getcwd()
            filename = os.path.join(base_dir, filename)
        if not os.path.exists(filename):
            raise Exception(f"File '{filename}' tidak ditemukan")
        with open(filename, 'r') as f:
            code = f.read()
        saved_node = self.current_node
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        try:
            self.eval_statements(ast.statements, env)
        finally:
            self.current_node = saved_node
        return None
        

    def eval_try(self, node, env):
        try:
            self.eval_statements(node.try_block, env)
        except (ReturnSignal, BreakSignal, ContinueSignal, ExitSignal):
            # Signal kontrol tidak boleh ditangkap oleh cubo
            raise
        except Exception as e:
            # Buat environment baru untuk handler
            handler_env = Environment(env)
            if node.error_var:
                handler_env.define(node.error_var, str(e))
            self.eval_statements(node.handler_block, handler_env)
        return None

    def run(self, ast):
        try:
            self.eval(ast, self.global_env)
        except ExitSignal:
            pass
        except ReturnSignal:
            pass
        except Exception as e:
            node = self.current_node
            if node and node.line is not None:
                print(f"Error pada baris {node.line}, kolom {node.column}: {e}")
            else:
                print(f"Error: {e}")