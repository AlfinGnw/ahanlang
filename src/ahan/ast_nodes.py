class ASTNode:
    def __init__(self):
        self.line = None
        self.column = None

class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class BooleanNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class NullNode(ASTNode):
    def __init__(self):
        super().__init__()

class ListNode(ASTNode):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

class VariableAccessNode(ASTNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

class AssignmentNode(ASTNode):
    def __init__(self, target, value, op=None):
        super().__init__()
        self.target = target   # string (nama variabel) atau ASTNode (IndexAccessNode)
        self.value = value
        self.op = op           # None untuk '=', atau operator dasar '+', '-', dst.

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        super().__init__()
        self.op = op
        self.operand = operand

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_body = else_body

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

class ForNode(ASTNode):
    def __init__(self, var_name, iterable, body):
        super().__init__()
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, body):
        super().__init__()
        self.name = name
        self.params = params
        self.body = body
        self.closure = None

class ReturnNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class CallNode(ASTNode):
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.args = args

class IndexAccessNode(ASTNode):
    def __init__(self, target, index):
        super().__init__()
        self.target = target
        self.index = index

class SliceNode(ASTNode):
    def __init__(self, target, start=None, end=None):
        super().__init__()
        self.target = target
        self.start = start
        self.end = end

class PrintNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class InputNode(ASTNode):
    def __init__(self, prompt=None):
        super().__init__()
        self.prompt = prompt

class BreakNode(ASTNode):
    def __init__(self):
        super().__init__()

class ContinueNode(ASTNode):
    def __init__(self):
        super().__init__()

class ExitNode(ASTNode):
    def __init__(self):
        super().__init__()

class ShowNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class ImportNode(ASTNode):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

class TryNode(ASTNode):
    def __init__(self, try_block, error_var, handler_block):
        super().__init__()
        self.try_block = try_block
        self.error_var = error_var    # nama variabel untuk pesan error, bisa None
        self.handler_block = handler_block
            
class BlockNode(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

class DictNode(ASTNode):
    def __init__(self, pairs):
        super().__init__()
        self.pairs = pairs  # list of (key_node, value_node)