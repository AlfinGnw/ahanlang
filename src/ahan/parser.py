from .token_types import *
from .ast_nodes import *
from .lexer import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(TT_EOF, None, -1, -1)

    def peek(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        else:
            return Token(TT_EOF, None, -1, -1)

    def expect(self, token_type, value=None):
        token = self.current_token
        if token.type != token_type or (value is not None and token.value != value):
            raise Exception(f"Token tidak sesuai: diharapkan {token_type} {value}, ditemukan {token} pada baris {token.line}, kolom {token.column}")
        self.advance()
        return token

    def expect_newline(self):
        if self.current_token.type == TT_NEWLINE:
            self.advance()
            while self.current_token.type == TT_NEWLINE:
                self.advance()
        elif self.current_token.type == TT_EOF:
            pass
        else:
            raise Exception(f"Diharapkan akhir baris, ditemukan {self.current_token} pada baris {self.current_token.line}")

    def _set_pos(self, node, token):
        if node is not None:
            node.line = token.line
            node.column = token.column
        return node

    def parse(self):
        statements = self.parse_block()
        self.expect(TT_EOF)
        return BlockNode(statements)

    def parse_block(self):
        statements = []
        while self.current_token.type != TT_EOF and self.current_token.type != TT_DEDENT:
            if self.current_token.type == TT_NEWLINE:
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            if isinstance(stmt, (IfNode, WhileNode, ForNode, FunctionDefNode, TryNode)):
                if self.current_token.type == TT_NEWLINE:
                    self.advance()
                    while self.current_token.type == TT_NEWLINE:
                        self.advance()
            else:
                if self.current_token.type == TT_NEWLINE:
                    self.advance()
                    while self.current_token.type == TT_NEWLINE:
                        self.advance()
                elif self.current_token.type not in (TT_DEDENT, TT_EOF):
                    raise Exception(f"Token tak terduga setelah pernyataan: {self.current_token}")
        return statements

    def parse_statement(self):
        start_token = self.current_token
        token = start_token

        # if / anga
        if token.type == TT_KEYWORD and token.value == 'anga':
            return self.parse_if()

        # while / salamo
        if token.type == TT_KEYWORD and token.value == 'salamo':
            return self.parse_while()

        # for / mek
        if token.type == TT_KEYWORD and token.value == 'mek':
            return self.parse_for()

        # function / fungsi
        if token.type == TT_KEYWORD and token.value == 'fungsi':
            return self.parse_function_def()

        # return / balekken
        if token.type == TT_KEYWORD and token.value in ('balekken', 'muba'):
            self.advance()
            expr = self.parse_expression() if self.current_token.type != TT_NEWLINE else None
            return self._set_pos(ReturnNode(expr), start_token)

        # print / kaluarken
        if token.type == TT_KEYWORD and token.value in ('kaluarken', 'ahan'):
            self.advance()
            expr = self.parse_expression() if self.current_token.type != TT_NEWLINE else None
            return self._set_pos(PrintNode(expr), start_token)

        # show / antoroman
        if token.type == TT_KEYWORD and token.value == 'antoroman':
            self.advance()
            expr = self.parse_expression() if self.current_token.type != TT_NEWLINE else None
            return self._set_pos(ShowNode(expr), start_token)

        # input / baco
        if token.type == TT_KEYWORD and token.value in ('baco', 'mitidao'):
            self.advance()
            prompt = None
            if self.current_token.type != TT_NEWLINE:
                prompt = self.parse_expression()
            return self._set_pos(InputNode(prompt), start_token)

        # exit / kaluar
        if token.type == TT_KEYWORD and token.value == 'kaluar':
            self.advance()
            return self._set_pos(ExitNode(), start_token)

        # break / kajab
        if token.type == TT_KEYWORD and token.value == 'kajab':
            self.advance()
            return self._set_pos(BreakNode(), start_token)

        # continue / lanjar
        if token.type == TT_KEYWORD and token.value == 'lanjar':
            self.advance()
            return self._set_pos(ContinueNode(), start_token)

        # import / pakek
        if token.type == TT_KEYWORD and token.value == 'pakek':
            self.advance()
            if self.current_token.type == TT_STRING:
                filename = self.current_token.value
                self.advance()
            elif self.current_token.type == TT_IDENTIFIER:
                filename = self.current_token.value
                self.advance()
            else:
                raise Exception(f"'pakek' harus diikuti nama file pada baris {token.line}")
            return self._set_pos(ImportNode(filename), start_token)

        # try / cubo
        if token.type == TT_KEYWORD and token.value == 'cubo':
            return self.parse_try()

        # Expression statement atau assignment
        expr = self.parse_expression()
        if self.current_token.type == TT_OPERATOR and self.current_token.value in ('=', '+=', '-=', '*=', '/=', '%=', '^='):
            op_token = self.current_token
            if not isinstance(expr, (VariableAccessNode, IndexAccessNode)):
                raise Exception(f"Target assignment tidak valid pada baris {op_token.line}, kolom {op_token.column}: hanya variabel atau elemen list/dict yang dapat di-assign")
            self.advance()
            value_expr = self.parse_expression()
            if op_token.value == '=':
                op = None
            else:
                op = op_token.value[:-1]
            return self._set_pos(AssignmentNode(expr, value_expr, op), start_token)
        return self._set_pos(expr, start_token)

    def parse_if(self):
        start_token = self.current_token
        self.advance()
        condition = self.parse_expression()
        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        body = self.parse_block()
        self.expect(TT_DEDENT)
        else_body = None
        if self.current_token.type == TT_KEYWORD and self.current_token.value == 'laenne':
            self.advance()
            if self.current_token.type == TT_KEYWORD and self.current_token.value == 'anga':
                nested_if = self.parse_if()
                else_body = [nested_if]
            else:
                self.expect(TT_COLON)
                self.expect_newline()
                self.expect(TT_INDENT)
                else_body = self.parse_block()
                self.expect(TT_DEDENT)
        return self._set_pos(IfNode(condition, body, else_body), start_token)

    def parse_while(self):
        start_token = self.current_token
        self.advance()
        condition = self.parse_expression()
        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        body = self.parse_block()
        self.expect(TT_DEDENT)
        return self._set_pos(WhileNode(condition, body), start_token)

    def parse_for(self):
        start_token = self.current_token
        self.advance()
        var_name = self.expect(TT_IDENTIFIER).value
        self.expect(TT_KEYWORD, 'bak')
        iterable = self.parse_expression()
        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        body = self.parse_block()
        self.expect(TT_DEDENT)
        return self._set_pos(ForNode(var_name, iterable, body), start_token)

    def parse_function_def(self):
        start_token = self.current_token
        self.advance()
        func_name = self.expect(TT_IDENTIFIER).value
        self.expect(TT_LPAREN)
        params = []
        if self.current_token.type != TT_RPAREN:
            params.append(self.expect(TT_IDENTIFIER).value)
            while self.current_token.type == TT_COMMA:
                self.advance()
                params.append(self.expect(TT_IDENTIFIER).value)
        self.expect(TT_RPAREN)
        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        body = self.parse_block()
        self.expect(TT_DEDENT)
        return self._set_pos(FunctionDefNode(func_name, params, body), start_token)

    def parse_try(self):
        start_token = self.current_token
        self.advance()
        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        try_block = self.parse_block()
        self.expect(TT_DEDENT)

        if not (self.current_token.type == TT_KEYWORD and self.current_token.value == 'adorapek'):
            raise Exception(f"'cubo' harus diikuti 'adorapek' pada baris {start_token.line}")
        self.advance()

        error_var = None
        if self.current_token.type == TT_IDENTIFIER:
            error_var = self.current_token.value
            self.advance()

        self.expect(TT_COLON)
        self.expect_newline()
        self.expect(TT_INDENT)
        handler_block = self.parse_block()
        self.expect(TT_DEDENT)

        return self._set_pos(TryNode(try_block, error_var, handler_block), start_token)

    # --- Ekspresi (dengan preseden) ---
    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.current_token.type == TT_KEYWORD and self.current_token.value == 'atau':
            op_token = self.current_token
            self.advance()
            right = self.parse_and()
            left = self._set_pos(BinaryOpNode(left, 'atau', right), op_token)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.current_token.type == TT_KEYWORD and self.current_token.value == 'dan':
            op_token = self.current_token
            self.advance()
            right = self.parse_not()
            left = self._set_pos(BinaryOpNode(left, 'dan', right), op_token)
        return left

    def parse_not(self):
        if self.current_token.type == TT_KEYWORD and self.current_token.value == 'teen':
            op_token = self.current_token
            self.advance()
            operand = self.parse_not()
            return self._set_pos(UnaryOpNode('teen', operand), op_token)
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_arithmetic()
        while (self.current_token.type == TT_OPERATOR and
               self.current_token.value in ('==', '!=', '<', '>', '<=', '>=')):
            op_token = self.current_token
            op = self.current_token.value
            self.advance()
            right = self.parse_arithmetic()
            left = self._set_pos(BinaryOpNode(left, op, right), op_token)
        return left

    def parse_arithmetic(self):
        left = self.parse_term()
        while (self.current_token.type == TT_OPERATOR and
               self.current_token.value in ('+', '-')):
            op_token = self.current_token
            op = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = self._set_pos(BinaryOpNode(left, op, right), op_token)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while (self.current_token.type == TT_OPERATOR and
               self.current_token.value in ('*', '/', '%')):
            op_token = self.current_token
            op = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = self._set_pos(BinaryOpNode(left, op, right), op_token)
        return left

    def parse_factor(self):
        return self.parse_pow()

    def parse_pow(self):
        left = self.parse_unary()
        if (self.current_token.type == TT_OPERATOR and
                self.current_token.value == '^'):
            op_token = self.current_token
            self.advance()
            right = self.parse_pow()
            left = self._set_pos(BinaryOpNode(left, '^', right), op_token)
        return left

    def parse_unary(self):
        token = self.current_token
        if token.type == TT_OPERATOR and token.value == '-':
            self.advance()
            operand = self.parse_unary()
            return self._set_pos(UnaryOpNode('-', operand), token)
        return self.parse_primary()

    def parse_primary(self):
        token = self.current_token

        if token.type == TT_NUMBER:
            self.advance()
            node = self._set_pos(NumberNode(token.value), token)
            return self.parse_postfix(node)
        if token.type == TT_STRING:
            self.advance()
            node = self._set_pos(StringNode(token.value), token)
            return self.parse_postfix(node)
        if token.type == TT_KEYWORD:
            if token.value in ('kaluarken', 'ahan', 'baco', 'mitidao'):
                name = token.value
                self.advance()
                if self.current_token.type == TT_LPAREN:
                    call_node = self.parse_call(name)
                    call_node = self._set_pos(call_node, token)
                    return self.parse_postfix(call_node)
                else:
                    raise Exception(f"Fungsi '{name}' harus diikuti '(' pada baris {token.line}")
            elif token.value == 'dise':
                self.advance()
                node = self._set_pos(BooleanNode(True), token)
                return self.parse_postfix(node)
            elif token.value == 'salah':
                self.advance()
                node = self._set_pos(BooleanNode(False), token)
                return self.parse_postfix(node)
            elif token.value == 'kosong':
                self.advance()
                node = self._set_pos(NullNode(), token)
                return self.parse_postfix(node)
            else:
                raise Exception(f"Keyword tidak valid sebagai ekspresi: {token.value} pada baris {token.line}")
        if token.type == TT_IDENTIFIER:
            name = token.value
            self.advance()
            node = VariableAccessNode(name)
            node = self._set_pos(node, token)
            return self.parse_postfix(node)
        if token.type == TT_LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TT_RPAREN)
            expr = self._set_pos(expr, token)
            return self.parse_postfix(expr)
        if token.type == TT_LBRACKET:
            return self.parse_postfix(self.parse_list())
        if token.type == TT_LBRACE:
            return self.parse_postfix(self.parse_dict())

        raise Exception(f"Token tak terduga dalam ekspresi: {token} pada baris {token.line}")

    def parse_postfix(self, node):
        while True:
            if self.current_token.type == TT_LPAREN:
                if isinstance(node, VariableAccessNode):
                    call_token = self.current_token
                    node = self.parse_call(node.name)
                    self._set_pos(node, call_token)
                else:
                    raise Exception("Hanya identifier yang bisa dipanggil sebagai fungsi")
            elif self.current_token.type == TT_LBRACKET:
                bracket_token = self.current_token
                self.advance()
                if self.current_token.type == TT_COLON:
                    start = None
                    self.advance()
                    if self.current_token.type != TT_RBRACKET:
                        end = self.parse_expression()
                    else:
                        end = None
                    self.expect(TT_RBRACKET)
                    slice_node = SliceNode(node, start, end)
                    node = self._set_pos(slice_node, bracket_token)
                else:
                    first = self.parse_expression()
                    if self.current_token.type == TT_COLON:
                        start = first
                        self.advance()
                        if self.current_token.type != TT_RBRACKET:
                            end = self.parse_expression()
                        else:
                            end = None
                        self.expect(TT_RBRACKET)
                        slice_node = SliceNode(node, start, end)
                        node = self._set_pos(slice_node, bracket_token)
                    else:
                        self.expect(TT_RBRACKET)
                        index_node = IndexAccessNode(node, first)
                        node = self._set_pos(index_node, bracket_token)
            else:
                break
        return node

    def parse_call(self, func_name):
        self.expect(TT_LPAREN)
        args = []
        if self.current_token.type != TT_RPAREN:
            args.append(self.parse_expression())
            while self.current_token.type == TT_COMMA:
                self.advance()
                args.append(self.parse_expression())
        self.expect(TT_RPAREN)
        return CallNode(func_name, args)

    def parse_list(self):
        start_token = self.current_token
        self.expect(TT_LBRACKET)
        elements = []
        if self.current_token.type != TT_RBRACKET:
            elements.append(self.parse_expression())
            while self.current_token.type == TT_COMMA:
                self.advance()
                elements.append(self.parse_expression())
        self.expect(TT_RBRACKET)
        return self._set_pos(ListNode(elements), start_token)

    def parse_dict(self):
        start_token = self.current_token
        self.expect(TT_LBRACE)
        pairs = []
        if self.current_token.type != TT_RBRACE:
            key = self.parse_expression()
            self.expect(TT_COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            while self.current_token.type == TT_COMMA:
                self.advance()
                key = self.parse_expression()
                self.expect(TT_COLON)
                value = self.parse_expression()
                pairs.append((key, value))
        self.expect(TT_RBRACE)
        return self._set_pos(DictNode(pairs), start_token)