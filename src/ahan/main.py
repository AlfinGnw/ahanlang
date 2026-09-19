"""Entry point untuk AHAN — REPL dan file runner."""

import sys
import os
import re
from .lexer import Lexer
from .parser import Parser
from .evaluator import Evaluator

__version__ = "0.1.0"

HELP_TEXT = """
AHAN — Bahasa Pemrograman Imperatif dengan Sintaks Bahasa Devayan

Penggunaan:
    ahan [opsi] [file.ahan]

Opsi:
    -h, --help      Tampilkan bantuan ini
    -v, --version   Tampilkan versi
    -r, --repl      Jalankan REPL interaktif
    -c, --code CODE Jalankan kode langsung dari string

Contoh:
    ahan program.ahan
    ahan --repl
    ahan -c 'ahan("Halo, Dunia!")'
""".strip()


def _format_parse_error(e):
    message = str(e)
    match = re.search(r"pada baris (\d+), kolom (\d+)", message)
    if match:
        line, column = match.groups()
        clean = message[:match.start()].strip(": ")
        return Exception(f"Error pada baris {line}, kolom {column}: {clean}")
    return Exception(message)


def run_code(code, evaluator=None, main_file=None):
    """Jalankan kode AHAN dari string."""
    if evaluator is None:
        evaluator = Evaluator(main_file)
    try:
        tokens = Lexer(code).tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
    except Exception as e:
        raise _format_parse_error(e)
    evaluator.run(ast)


def run_file(filename):
    """Jalankan file AHAN dengan deteksi encoding otomatis."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' tidak ditemukan.", file=sys.stderr)
        sys.exit(1)

    # Baca file sebagai bytes
    with open(filename, 'rb') as f:
        raw = f.read()

    # Coba beberapa encoding
    code = None
    for enc in ('utf-8-sig', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1'):
        try:
            code = raw.decode(enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if code is None:
        print(f"Error: Tidak dapat membaca file '{filename}' (encoding tidak dikenal).", file=sys.stderr)
        sys.exit(1)

    run_code(code, main_file=filename)


def _is_block_start(line):
    stripped = line.split('#')[0].rstrip()
    return stripped.endswith(':')


def repl():
    """Jalankan REPL interaktif AHAN."""
    evaluator = Evaluator()
    print(f"AHAN REPL v{__version__}")
    print("Ketik 'kaluar' atau Ctrl+D untuk keluar.")
    print("Untuk blok multi-baris, akhiri dengan baris kosong.")
    print()

    while True:
        try:
            try:
                line = input("ahan> ")
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print("\n(dibatalkan)")
                continue

            if line.strip() == 'kaluar':
                break
            if line.strip() == '':
                continue

            buffer = [line]

            if _is_block_start(line):
                indent = 4
                while True:
                    prompt = "   ...  " + " " * indent
                    try:
                        continuation = input(prompt)
                    except EOFError:
                        break
                    except KeyboardInterrupt:
                        print("\n(dibatalkan)")
                        buffer = []
                        break

                    if continuation.strip() == '':
                        break

                    if continuation.startswith(' ') or continuation.startswith('\t'):
                        buffer.append(continuation)
                        stripped = continuation.lstrip(' \t')
                        actual_indent = len(continuation) - len(stripped)
                        if _is_block_start(continuation):
                            indent = actual_indent + 4
                        else:
                            indent = actual_indent
                    else:
                        buffer.append(' ' * indent + continuation)
                        if _is_block_start(continuation):
                            indent += 4

            code = '\n'.join(buffer)
            if code.strip() == '':
                continue
            try:
                run_code(code, evaluator)
            except Exception as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\n(dibatalkan)")
            continue


def cli():
    """Entry point utama untuk command line."""
    args = sys.argv[1:]

    if not args:
        repl()
        return

    # Cek flag pertama
    first = args[0]

    if first in ('-h', '--help'):
        print(HELP_TEXT)
        return

    if first in ('-v', '--version'):
        print(f"AHAN v{__version__}")
        return

    if first in ('-r', '--repl'):
        repl()
        return

    if first in ('-c', '--code'):
        if len(args) < 2:
            print("Error: Opsi -c/--code memerlukan argumen kode.", file=sys.stderr)
            sys.exit(1)
        code = args[1]
        try:
            run_code(code)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Anggap sebagai nama file
    filename = first
    try:
        run_file(filename)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli()