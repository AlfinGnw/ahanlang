import pytest

from ahan.lexer import Lexer
from ahan.main import run_code


def _token_values(code):
    return [(t.type, t.value) for t in Lexer(code).tokenize()]


def _run(code):
    run_code(code)


@pytest.fixture
def run():
    """Jalankan kode AHAN, kembalikan fungsi (kode) yang mengembalikan stdout."""
    def _run_and_capture(code):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            run_code(code)
        return buf.getvalue()
    return _run_and_capture


@pytest.fixture
def run_error():
    """Jalankan kode AHAN yang menghasilkan error, kembalikan pesan error."""
    def _run_and_get_error(code):
        import contextlib
        import io
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                run_code(code)
        except Exception as e:
            return buf.getvalue() + str(e)
        return buf.getvalue()
    return _run_and_get_error