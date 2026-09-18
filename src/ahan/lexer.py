from .token_types import *

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, text):
        # Hapus BOM jika ada
        if text.startswith('\ufeff'):
            text = text[1:]
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if self.text else None
        self.indent_stack = [0]
        self.at_line_start = True
        self.pending_indent_tokens = []
        self.bracket_depth = 0

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in (' ', '\t', '\r'):
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def make_number(self):
        num_str = ''
        is_float = False
        start_column = self.column
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    raise Exception(f"Format angka tidak valid di baris {self.line}, kolom {self.column}")
                is_float = True
            num_str += self.current_char
            self.advance()
        if is_float:
            return Token(TT_NUMBER, float(num_str), self.line, start_column)
        else:
            return Token(TT_NUMBER, int(num_str), self.line, start_column)

    def make_string(self, quote_char):
        string_val = ''
        start_line = self.line
        start_col = self.column
        self.advance()  # lewati kutip pembuka
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    string_val += '\n'
                elif self.current_char == 't':
                    string_val += '\t'
                elif self.current_char == '\\':
                    string_val += '\\'
                elif self.current_char == quote_char:
                    string_val += quote_char
                else:
                    string_val += '\\' + self.current_char
                self.advance()
            else:
                string_val += self.current_char
                self.advance()
        if self.current_char != quote_char:
            raise Exception(f"String tidak ditutup mulai baris {start_line}, kolom {start_col}")
        self.advance()
        return Token(TT_STRING, string_val, start_line, start_col)

    def make_identifier_or_keyword(self):
        id_str = ''
        start_col = self.column
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        keywords = {
            'anga', 'laenne', 'salamo', 'mek', 'dan', 'atau', 'teen',
            'dise', 'salah', 'kosong', 'fungsi', 'balekken', 'kaluarken',
            'baco', 'bak', 'kajab', 'lanjar',
            'ahan', 'mitidao', 'muba', 'kaluar', 'antoroman', 'pakek',
            'cubo', 'adorapek'
        }
        if id_str in keywords:
            return Token(TT_KEYWORD, id_str, self.line, start_col)
        else:
            return Token(TT_IDENTIFIER, id_str, self.line, start_col)

    def get_next_token(self):
        # Jika ada pending indent tokens, keluarkan satu per satu
        if self.pending_indent_tokens:
            return self.pending_indent_tokens.pop(0)

        # ===== Penanganan awal baris =====
        if self.at_line_start and self.bracket_depth > 0:
            # Di dalam bracket: lewati spasi awal, jangan hitung indentasi
            self.at_line_start = False
            while self.current_char in (' ', '\t'):
                self.advance()

        if self.at_line_start and self.bracket_depth == 0:
            self.at_line_start = False

            # Hitung indentasi
            indent_level = 0
            while self.current_char == ' ':
                indent_level += 1
                self.advance()

            # Baris kosong
            if self.current_char in ('\n', None):
                if self.current_char == '\n':
                    token = Token(TT_NEWLINE, '\n', self.line, self.column)
                    self.advance()
                    self.at_line_start = True
                    return token
                else:  # EOF
                    if len(self.indent_stack) > 1:
                        self.indent_stack.pop()
                        return Token(TT_DEDENT, self.indent_stack[-1], self.line, self.column)
                    return Token(TT_EOF, None, self.line, self.column)

            # Baris komentar
            elif self.current_char == '#':
                self.skip_comment()
                if self.current_char == '\n':
                    token = Token(TT_NEWLINE, '\n', self.line, self.column)
                    self.advance()
                    self.at_line_start = True
                    return token
                else:
                    if len(self.indent_stack) > 1:
                        self.indent_stack.pop()
                        return Token(TT_DEDENT, self.indent_stack[-1], self.line, self.column)
                    return Token(TT_EOF, None, self.line, self.column)

            # Baris berisi kode: bandingkan indentasi
            else:
                current_indent = indent_level
                top = self.indent_stack[-1]
                indent_tokens = []
                if current_indent > top:
                    self.indent_stack.append(current_indent)
                    indent_tokens.append(Token(TT_INDENT, current_indent, self.line, self.column))
                elif current_indent < top:
                    while self.indent_stack and current_indent < self.indent_stack[-1]:
                        self.indent_stack.pop()
                        indent_tokens.append(Token(TT_DEDENT, self.indent_stack[-1] if self.indent_stack else 0, self.line, self.column))
                    if current_indent != self.indent_stack[-1]:
                        raise Exception(f"Indentasi tidak konsisten pada baris {self.line}, kolom {self.column}")
                if indent_tokens:
                    self.pending_indent_tokens = indent_tokens[1:]
                    return indent_tokens[0]

        # ===== Proses karakter normal =====
        # Lewati spasi dalam baris
        if self.current_char in (' ', '\t', '\r'):
            self.skip_whitespace()

        # Komentar di tengah baris
        if self.current_char == '#':
            self.skip_comment()
            if self.current_char == '\n':
                token = Token(TT_NEWLINE, '\n', self.line, self.column)
                self.advance()
                self.at_line_start = True
                return token
            else:
                if len(self.indent_stack) > 1:
                    self.indent_stack.pop()
                    return Token(TT_DEDENT, self.indent_stack[-1], self.line, self.column)
                return Token(TT_EOF, None, self.line, self.column)

        # Newline
        if self.current_char == '\n':
            if self.bracket_depth > 0:
                # Di dalam bracket: newline diabaikan
                self.advance()
                return self.get_next_token()
            token = Token(TT_NEWLINE, '\n', self.line, self.column)
            self.advance()
            self.at_line_start = True
            return token

        # EOF
        if self.current_char is None:
            if len(self.indent_stack) > 1:
                self.indent_stack.pop()
                return Token(TT_DEDENT, self.indent_stack[-1], self.line, self.column)
            return Token(TT_EOF, None, self.line, self.column)

        # Angka (termasuk desimal yang diawali titik, misal .5)
        if self.current_char.isdigit() or (
            self.current_char == '.' and self.peek() is not None and self.peek().isdigit()
        ):
            return self.make_number()

        # String
        if self.current_char in ('"', "'"):
            return self.make_string(self.current_char)

        # Identifier atau keyword
        if self.current_char.isalpha() or self.current_char == '_':
            return self.make_identifier_or_keyword()

        # ===== Operator gabungan (harus dicek sebelum operator tunggal) =====
        if self.current_char == '+':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '+=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '+', self.line, self.column - 1)
        if self.current_char == '-':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '-=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '-', self.line, self.column - 1)
        if self.current_char == '*':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '*=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '*', self.line, self.column - 1)
        if self.current_char == '/':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '/=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '/', self.line, self.column - 1)
        if self.current_char == '%':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '%=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '%', self.line, self.column - 1)
        if self.current_char == '^':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '^=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '^', self.line, self.column - 1)

        # ===== Operator perbandingan dan assignment =====
        if self.current_char == '=':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '==', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '=', self.line, self.column - 1)
        if self.current_char == '!':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '!=', self.line, self.column - 2)
            raise Exception(f"Karakter '!' harus diikuti '=' pada baris {self.line}, kolom {self.column}")
        if self.current_char == '<':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '<=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '<', self.line, self.column - 1)
        if self.current_char == '>':
            if self.peek() == '=':
                self.advance(); self.advance()
                return Token(TT_OPERATOR, '>=', self.line, self.column - 2)
            self.advance()
            return Token(TT_OPERATOR, '>', self.line, self.column - 1)

        # ===== Bracket, kurung, kurawal =====
        if self.current_char == '(':
            self.advance()
            self.bracket_depth += 1
            return Token(TT_LPAREN, '(', self.line, self.column - 1)
        if self.current_char == ')':
            self.advance()
            self.bracket_depth -= 1
            if self.bracket_depth < 0:
                self.bracket_depth = 0
            return Token(TT_RPAREN, ')', self.line, self.column - 1)
        if self.current_char == '[':
            self.advance()
            self.bracket_depth += 1
            return Token(TT_LBRACKET, '[', self.line, self.column - 1)
        if self.current_char == ']':
            self.advance()
            self.bracket_depth -= 1
            if self.bracket_depth < 0:
                self.bracket_depth = 0
            return Token(TT_RBRACKET, ']', self.line, self.column - 1)
        if self.current_char == '{':
            self.advance()
            self.bracket_depth += 1
            return Token(TT_LBRACE, '{', self.line, self.column - 1)
        if self.current_char == '}':
            self.advance()
            self.bracket_depth -= 1
            if self.bracket_depth < 0:
                self.bracket_depth = 0
            return Token(TT_RBRACE, '}', self.line, self.column - 1)

        # ===== Tanda baca =====
        if self.current_char == ',':
            self.advance()
            return Token(TT_COMMA, ',', self.line, self.column - 1)
        if self.current_char == ':':
            self.advance()
            return Token(TT_COLON, ':', self.line, self.column - 1)

        # Karakter tidak dikenal
        raise Exception(f"Karakter tidak dikenal '{self.current_char}' pada baris {self.line}, kolom {self.column}")

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TT_EOF:
                break
        return tokens