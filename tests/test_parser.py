import pytest

from ahan.lexer import Lexer
from ahan.parser import Parser
from ahan.ast_nodes import (
    AssignmentNode, BinaryOpNode, UnaryOpNode, IfNode, WhileNode, ForNode,
    FunctionDefNode, CallNode, IndexAccessNode, SliceNode, PrintNode,
    ListNode, DictNode, VariableAccessNode, BlockNode, NumberNode,
)


def _parse(code):
    return Parser(Lexer(code).tokenize()).parse()


def _expr(code):
    ast = _parse(code)
    node = ast.statements[0]
    return node.value


def test_empty_program():
    ast = _parse("")
    assert isinstance(ast, BlockNode)
    assert ast.statements == []


def test_parse_number_expression():
    ast = _parse("x = 5")
    assert isinstance(ast.statements[0], AssignmentNode)
    assert isinstance(ast.statements[0].target, VariableAccessNode)
    assert ast.statements[0].target.name == "x"
    assert isinstance(ast.statements[0].value, NumberNode)


def test_parse_assignment_to_index():
    ast = _parse("a[0] = 5")
    stmt = ast.statements[0]
    assert isinstance(stmt, AssignmentNode)
    assert isinstance(stmt.target, IndexAccessNode)


def test_invalid_assignment_target_rejected():
    with pytest.raises(Exception) as excinfo:
        _parse("1 + 2 = 5")
    assert "Target assignment tidak valid" in str(excinfo.value)


def test_invalid_assignment_target_string_literal():
    with pytest.raises(Exception):
        _parse('"abc" = 5')


def test_power_right_associative_tree():
    stmt = _parse("2 ^ 3 ^ 2").statements[0]
    expr = stmt
    assert isinstance(expr, BinaryOpNode)
    assert expr.op == "^"
    assert isinstance(expr.left, NumberNode)
    assert isinstance(expr.right, BinaryOpNode)  # kanan juga berisi ^


def test_unary_minus_binds_tighter_than_pow():
    stmt = _parse("- 3 ^ 2").statements[0]
    expr = stmt
    assert isinstance(expr, BinaryOpNode)
    assert expr.op == "^"
    assert isinstance(expr.left, UnaryOpNode)
    assert expr.left.op == "-"


def test_precedence_mul_over_add():
    stmt = _parse("1 + 2 * 3").statements[0]
    expr = stmt
    assert isinstance(expr, BinaryOpNode)
    assert expr.op == "+"
    assert isinstance(expr.right, BinaryOpNode)
    assert expr.right.op == "*"


def test_postfix_string_literal():
    stmt = _parse('kaluarken "ab"[0]').statements[0]
    assert isinstance(stmt, PrintNode)
    assert isinstance(stmt.value, IndexAccessNode)


def test_postfix_list_literal():
    stmt = _parse("kaluarken [1, 2, 3][0]").statements[0]
    assert isinstance(stmt.value, IndexAccessNode)


def test_postfix_parenthesized():
    stmt = _parse("kaluarken (x)[0]").statements[0]
    assert isinstance(stmt.value, IndexAccessNode)
    assert isinstance(stmt.value.target, VariableAccessNode)


def test_postfix_chained():
    stmt = _parse("kaluarken m[1][0]").statements[0]
    outer = stmt.value
    assert isinstance(outer, IndexAccessNode)
    assert isinstance(outer.target, IndexAccessNode)


def test_slice_node():
    stmt = _parse("kaluarken daftar[1:3]").statements[0]
    assert isinstance(stmt.value, SliceNode)
    assert stmt.value.start is not None
    assert stmt.value.end is not None


def test_call_node():
    stmt = _parse("tambah(2, 3)").statements[0]
    assert isinstance(stmt, CallNode)
    assert stmt.func_name == "tambah"
    assert len(stmt.args) == 2


def test_function_def():
    stmt = _parse("fungsi f(a, b):\n    balekken a + b\n").statements[0]
    assert isinstance(stmt, FunctionDefNode)
    assert stmt.name == "f"
    assert stmt.params == ["a", "b"]


def test_if_else():
    code = ("anga x > 1:\n    ahan(1)\n"
            "laenne anga x > 0:\n    ahan(2)\n"
            "laenne:\n    ahan(3)\n")
    stmt = _parse(code).statements[0]
    assert isinstance(stmt, IfNode)
    assert stmt.else_body is not None
    assert isinstance(stmt.else_body[0], IfNode)  # laenne anga -> nested if


def test_while():
    stmt = _parse("salamo dise:\n    kajab\n").statements[0]
    assert isinstance(stmt, WhileNode)


def test_for():
    stmt = _parse("mek item bak [1, 2]:\n    ahan(item)\n").statements[0]
    assert isinstance(stmt, ForNode)
    assert stmt.var_name == "item"


def test_list_node():
    stmt = _parse("x = [1, 2]").statements[0]
    assert isinstance(stmt.value, ListNode)


def test_dict_node():
    stmt = _parse('x = {"a": 1}').statements[0]
    assert isinstance(stmt.value, DictNode)


def test_multiple_statements_same_line_rejected():
    with pytest.raises(Exception):
        _parse("x = 1 y = 2")


def test_unterminated_string_error():
    with pytest.raises(Exception) as excinfo:
        _parse('kaluarken "abc')
    assert "tidak ditutup" in str(excinfo.value)


def test_unknown_keyword_as_expression_error():
    with pytest.raises(Exception):
        _parse("salamo dise:")