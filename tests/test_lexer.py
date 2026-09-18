from ahan.lexer import Lexer
from ahan.token_types import (
    TT_NUMBER, TT_STRING, TT_IDENTIFIER, TT_KEYWORD, TT_OPERATOR,
    TT_LPAREN, TT_RPAREN, TT_LBRACKET, TT_RBRACKET, TT_LBRACE, TT_RBRACE,
    TT_COMMA, TT_COLON, TT_NEWLINE, TT_INDENT, TT_DEDENT, TT_EOF,
)


def _tokens(code):
    return Lexer(code).tokenize()


def _types(code):
    return [t.type for t in _tokens(code)]


def _values(code):
    return [(t.type, t.value) for t in _tokens(code)]


def test_integer():
    tok = _tokens("42")[0]
    assert tok.type == TT_NUMBER
    assert tok.value == 42


def test_float():
    tok = _tokens("3.14")[0]
    assert tok.type == TT_NUMBER
    assert tok.value == 3.14


def test_float_leading_dot():
    tok = _tokens(".5")[0]
    assert tok.type == TT_NUMBER
    assert tok.value == 0.5


def test_float_trailing_dot():
    tok = _tokens("5.")[0]
    assert tok.type == TT_NUMBER
    assert tok.value == 5.0


def test_double_quote_string():
    assert _values('"halo"')[0] == (TT_STRING, "halo")


def test_single_quote_string():
    assert _values("'halo'")[0] == (TT_STRING, "halo")


def test_string_escape_newline():
    assert _values('"a\\nb"')[0] == (TT_STRING, "a\nb")


def test_string_escape_tab():
    assert _values("'a\\tb'")[0] == (TT_STRING, "a\tb")


def test_string_escaped_quote():
    assert _values("'it\\'s'")[0] == (TT_STRING, "it's")
    assert _values('"say \\"hi\\""')[0] == (TT_STRING, 'say "hi"')


def test_string_unescaped_single_inside_double():
    assert _values('"it\'s"')[0] == (TT_STRING, "it's")


def test_identifier_and_keyword():
    values = _values("nama anga")
    assert values[0] == (TT_IDENTIFIER, "nama")
    assert values[1] == (TT_KEYWORD, "anga")


def test_keywords():
    keywords = ["anga", "laenne", "salamo", "mek", "dan", "atau", "teen",
                "dise", "salah", "kosong", "fungsi", "balekken", "kaluarken",
                "baco", "bak", "kajab", "lanjar", "ahan", "mitidao", "muba",
                "kaluar", "antoroman", "pakek", "cubo", "adorapek"]
    types = _types(" ".join(keywords))
    assert all(t == TT_KEYWORD for t in types[:len(keywords)])


def test_operators():
    assert [v for t, v in _values("+ - * / % ^ == != < > <= >= =") if v != None] == [
        "+", "-", "*", "/", "%", "^", "==", "!=", "<", ">", "<=", ">=", "=",
    ]


def test_compound_operators():
    assert [v for t, v in _values("+= -= *= /= %= ^=") if v != None] == [
        "+=", "-=", "*=", "/=", "%=", "^=",
    ]


def test_brackets_and_punctuation():
    types = [t for t in _types("( ) [ ] { } , :") if t != TT_EOF]
    assert types == [
        TT_LPAREN, TT_RPAREN, TT_LBRACKET, TT_RBRACKET,
        TT_LBRACE, TT_RBRACE, TT_COMMA, TT_COLON,
    ]


def test_indentation():
    code = "anga dise:\n    ahan(1)\nahan(2)\n"
    types = _types(code)
    assert TT_INDENT in types
    assert TT_DEDENT in types


def test_multipe_dedent():
    code = "anga dise:\n    salamo dise:\n        ahan(1)\nahan(2)\n"
    types = _types(code)
    assert types.count(TT_DEDENT) == 2


def test_multiline_list_ignores_newlines():
    code = "x = [1,\n2,\n3]\n"
    values = _values(code)
    tokens_inside = values[2:9]  # [1,\n2,\n3]
    assert TT_NEWLINE not in [t for t, v in tokens_inside]
    assert all(t == TT_COMMA or t == TT_NUMBER or t == TT_LBRACKET or t == TT_RBRACKET
               for t, v in tokens_inside)


def test_comment_line():
    types = _types("# komentar saja\nahan(1)\n")
    assert TT_KEYWORD in types  # ahan terbaca sebagai keyword


def test_inline_comment():
    tokens = _tokens("x = 1  # komentar\n")
    assert tokens[-1].type == TT_EOF
    assert TT_IDENTIFIER in [t.type for t in tokens]
    assert (TT_OPERATOR, "#") not in _values("x = 1  # komentar\n")


def test_unknown_character():
    try:
        _tokens("x @ 1")
    except Exception as e:
        assert "@" in str(e)
    else:
        raise AssertionError("harus error untuk karakter tidak dikenal")


def test_eof_position():
    tokens = _tokens("x")
    assert tokens[-1].type == TT_EOF


def test_line_and_column():
    tok = _tokens("12")[0]
    assert tok.line == 1
    assert tok.column == 1