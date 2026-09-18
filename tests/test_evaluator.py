import pytest


# --- Aritmetika & operator ---

def test_arithmetic(run):
    assert run("kaluarken 1 + 2 * 3").strip() == "7"
    assert run("kaluarken (1 + 2) * 3").strip() == "9"
    assert run("kaluarken 10 / 4").strip() == "2.5"
    assert run("kaluarken 10 % 3").strip() == "1"


def test_power_right_associative(run):
    assert run("kaluarken 2 ^ 3 ^ 2").strip() == "512"


def test_unary_minus(run):
    assert run("kaluarken -5").strip() == "-5"
    assert run("kaluarken 2 ^ - 1").strip() == "0.5"


def test_float_literals(run):
    assert run("kaluarken .5 + .5").strip() == "1.0"
    assert run("kaluarken 2.5 ^ 2").strip() == "6.25"


def test_string_concat(run):
    assert run('kaluarken "a" + "b"').strip() == "ab"


def test_comparison_and_logic(run):
    assert run("kaluarken 1 < 2").strip() == "dise"
    assert run("kaluarken 2 == 2").strip() == "dise"
    assert run("kaluarken 2 != 3").strip() == "dise"
    assert run("kaluarken dise dan salah").strip() == "salah"
    assert run("kaluarken dise atau salah").strip() == "dise"
    assert run("kaluarken teen dise").strip() == "salah"


def test_boolean_print_format(run):
    assert run("kaluarken dise").strip() == "dise"
    assert run("kaluarken salah").strip() == "salah"


# --- List & dictionary ---

def test_list_operations(run):
    out = run("daftar = [10, 20, 30]\n"
              "kaluarken daftar[0]\n"
              "daftar[1] = 99\n"
              "kaluarken daftar")
    assert out == "10\n[10, 99, 30]\n"


def test_negative_index(run):
    assert run("daftar = [10, 20, 30]\nkaluarken daftar[-1]").strip() == "30"
    assert run("daftar = [10, 20, 30]\nkaluarken daftar[-3]").strip() == "10"


def test_negative_index_assignment(run):
    out = run("daftar = [10, 20, 30]\n"
              "daftar[-1] = 40\n"
              "kaluarken daftar")
    assert out.strip() == "[10, 20, 40]"


def test_negative_index_string(run):
    assert run('teks = "abc"\nkaluarken teks[-1]').strip() == "c"


def test_negative_index_out_of_range_error(run_error):
    out = run_error("daftar = [10, 20]\nkaluarken daftar[-5]")
    assert "di luar jangkauan" in out


def test_slice(run):
    assert run("kaluarken [1, 2, 3, 4][1:3]").strip() == "[2, 3]"
    assert run('kaluarken "abcdef"[2:]').strip() == "cdef"


def test_postfix_on_literals(run):
    assert run('kaluarken "ab"[0]').strip() == "a"
    assert run("kaluarken [1, 2, 3][0]").strip() == "1"
    assert run("kaluarken ([1, 2, 3])[1]").strip() == "2"


def test_chained_index(run):
    assert run("m = [[1, 2], [3, 4]]\nkaluarken m[1][0]").strip() == "3"


def test_dict_operations(run):
    out = run('orang = {"nama": "Alfin", "umur": 25}\n'
              'kaluarken orang["nama"]\n'
              'orang["umur"] += 1\n'
              'kaluarken orang["umur"]')
    assert out == "Alfin\n26\n"


def test_dict_builtins(run):
    assert run('d = {"a": 1, "b": 2}\nkaluarken kunci(d)').strip() == "['a', 'b']"
    out = run('d = {"a": 1, "b": 2}\nkaluarken nilai(d)\nkaluarken pasangan(d)')
    assert out == "[1, 2]\n[['a', 1], ['b', 2]]\n"


def test_abek_negative_index(run):
    out = run("daftar = [10, 20, 30]\n"
              "kaluarken abek(daftar, -1, 999)\n"
              "kaluarken abek(daftar, -50, 999)")
    assert out == "30\n999\n"


# --- Assignment ---

def test_compound_assignment(run):
    out = run("x = 10\nx += 5\nx *= 2\nx ^= 3\nkaluarken x")
    assert out.strip() == "27000"


def test_invalid_assignment_target_error(run_error):
    out = run_error("1 + 2 = 5")
    assert "Target assignment tidak valid" in out


# --- Alur kontrol ---

def test_if_else(run):
    out = run("x = 5\n"
              "anga x > 5:\n"
              "    kaluarken \"besar\"\n"
              "laenne anga x > 0:\n"
              "    kaluarken \"sedang\"\n"
              "laenne:\n"
              "    kaluarken \"kecil\"")
    assert out.strip() == "sedang"


def test_while_loop(run):
    out = run("i = 0\nsalamo i < 3:\n    kaluarken i\n    i += 1")
    assert out == "0\n1\n2\n"


def test_for_loop(run):
    out = run("mek item bak [1, 2, 3]:\n    kaluarken item")
    assert out == "1\n2\n3\n"


def test_break_continue(run):
    out = run("i = 0\n"
              "salamo dise:\n"
              "    i += 1\n"
              "    anga i == 2:\n"
              "        lanjar\n"
              "    anga i >= 4:\n"
              "        kajab\n"
              "    kaluarken i")
    assert out == "1\n3\n"


def test_exit(run):
    out = run("kaluarken 1\nkaluar\nkaluarken 2")
    assert out.strip() == "1"


# --- Fungsi ---

def test_function_call(run):
    out = run("fungsi tambah(a, b):\n    balekken a + b\nkaluarken tambah(2, 3)")
    assert out.strip() == "5"


def test_function_scope(run):
    out = run("x = 10\n"
              "fungsi f():\n"
              "    x = 20\n"
              "    balekken x\n"
              "kaluarken f()\n"
              "kaluarken x")
    assert out == "20\n20\n"


def test_inner_function_mutates_parent(run):
    out = run("x = [1]\n"
              "fungsi f():\n"
              "    x[0] = 99\n"
              "f()\n"
              "kaluarken x")
    assert out.strip() == "[99]"


def test_recursion(run):
    out = run("fungsi faktorial(n):\n"
              "    anga n <= 1:\n"
              "        balekken 1\n"
              "    laenne:\n"
              "        balekken n * faktorial(n - 1)\n"
              "kaluarken faktorial(6)")
    assert out.strip() == "720"


def test_closure(run):
    out = run("fungsi pembuat_kali(faktor):\n"
              "    fungsi kali(x):\n"
              "        balekken x * faktor\n"
              "    balekken kali\n"
              "kali_dua = pembuat_kali(2)\n"
              "kaluarken kali_dua(10)")
    assert out.strip() == "20"


def test_call_postfix_index(run):
    out = run("fungsi ambil(x):\n    balekken x\nkaluarken ambil([7, 8, 9])[2]")
    assert out.strip() == "9"


# --- Input/output ---

def test_show_no_newline(run):
    out = run("antoroman \"halo\"\nantoroman \"dunia\"")
    assert out == "halodunia"


def test_input(run, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "42")
    out = run("x = baco()\nkaluarken x")
    assert out.strip() == "42"


def test_print_null(run):
    assert run("kaluarken kosong").strip() == "kosong"


# --- Error handling ---

def test_try_except(run):
    out = run("cubo:\n"
              "    x = int(\"abc\")\n"
              "adorapek pesan:\n"
              "    kaluarken \"gagal: \" + pesan")
    assert "gagal:" in out


def test_try_except_no_error(run):
    out = run("cubo:\n    x = 5\nadorapek:\n    kaluarken \"tidak boleh\"\nkaluarken x")
    assert out.strip() == "5"


def test_division_by_zero_raises(run_error):
    out = run_error("kaluarken 1 / 0")
    assert "Pembagian oleh nol" in out


def test_undefined_variable_error(run_error):
    out = run_error("kaluarken belum_didefinisikan")
    assert "tidak ditemukan" in out


def test_index_out_of_range_error(run_error):
    out = run_error("daftar = [1, 2]\nkaluarken daftar[5]")
    assert "di luar jangkauan" in out


def test_break_outside_loop():
    from ahan.main import run_code
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run_code("kajab")
    assert "Error" in buf.getvalue()