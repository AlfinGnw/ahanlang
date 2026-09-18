# Arsitektur AHAN

Dokumen ini menjelaskan bagaimana interpreter AHAN bekerja secara internal.

## Gambaran Umum

AHAN menggunakan arsitektur **tree-walking interpreter** klasik:

```
Kode Sumber  →  Lexer  →  Token  →  Parser  →  AST  →  Evaluator  →  Output
```

| File | Peran |
|------|-------|
| `token_types.py` | Definisi konstanta jenis token |
| `lexer.py` | Tokenisasi kode sumber |
| `ast_nodes.py` | Definisi node AST |
| `parser.py` | Pembangunan AST dari token |
| `evaluator.py` | Eksekusi AST |
| `main.py` | Entry point (REPL dan file runner) |

---

## 1. Lexer (`lexer.py`)

### Tugas
Mengubah string kode sumber menjadi daftar objek `Token`.

### Struktur Token

```python
class Token:
    type: str      # NUMBER, STRING, IDENTIFIER, KEYWORD, OPERATOR, dst.
    value: Any     # nilai literal atau simbol
    line: int      # nomor baris (1-indexed)
    column: int    # nomor kolom (1-indexed)
```

### Tantangan Utama

#### a. Indentasi Signifikan

Seperti Python, AHAN menggunakan indentasi untuk menandai blok kode. Lexer memelihara `indent_stack`:

- Baris dengan indentasi lebih dalam → emit `INDENT`
- Baris dengan indentasi lebih dangkal → emit satu atau lebih `DEDENT`
- Baris kosong dan komentar diabaikan untuk keperluan indentasi

#### b. Bracket Tracking

Untuk memungkinkan list, dictionary, dan pemanggilan fungsi multi-baris, lexer melacak `bracket_depth`:

- Saat `bracket_depth > 0`, karakter `\n` diabaikan.
- Indentasi di dalam bracket tidak memengaruhi `indent_stack`.

Ini memungkinkan:

```
orang = {
    "nama": "Alfin",
    "umur": 25
}
```

#### c. String Escape

String mendukung escape sequence: `\n`, `\t`, `\\`, `\'`, `\"`.

### Alur `get_next_token()`

1. Jika ada `pending_indent_tokens`, keluarkan satu.
2. Jika di awal baris dan di dalam bracket, lewati spasi.
3. Jika di awal baris dan tidak di dalam bracket, hitung indentasi dan bandingkan dengan `indent_stack`.
4. Lewati spasi dan komentar.
5. Tangani newline (abaikan jika di dalam bracket).
6. Tangani EOF, angka, string, identifier/keyword, operator, bracket, tanda baca.

---

## 2. Parser (`parser.py`)

### Tugas
Mengubah daftar token menjadi AST.

### Teknik
**Recursive descent parsing** dengan hierarki preseden operator:

```
parse_expression
  └─ parse_or            (atau)
      └─ parse_and       (dan)
          └─ parse_not   (teen)
              └─ parse_comparison   (== != < > <= >=)
                  └─ parse_arithmetic   (+ -)
                      └─ parse_term      (* / %)
                          └─ parse_factor  (^)
                              └─ parse_unary  (-)
                                  └─ parse_primary
                                      └─ parse_postfix  (pemanggilan, indexing)
```

### Pernyataan (Statement)

Setiap pernyataan di-parse oleh `parse_statement()`, yang memeriksa kata kunci awal:

| Kata Kunci | Node |
|------------|------|
| `anga` | `IfNode` |
| `salamo` | `WhileNode` |
| `mek` | `ForNode` |
| `fungsi` | `FunctionDefNode` |
| `balekken`/`muba` | `ReturnNode` |
| `ahan`/`kaluarken` | `PrintNode` |
| `baco`/`mitidao` | `InputNode` |
| `antoroman` | `ShowNode` |
| `kaluar` | `ExitNode` |
| `kajab` | `BreakNode` |
| `lanjar` | `ContinueNode` |
| `pakek` | `ImportNode` |
| `cubo` | `TryNode` |
| lainnya | ekspresi atau assignment |

### Penyimpanan Posisi

Setiap node AST menyimpan `line` dan `column` dari token awalnya, digunakan untuk pesan error runtime.

---

## 3. AST (`ast_nodes.py`)

### Hierarki Node

```
ASTNode
├── NumberNode
├── StringNode
├── BooleanNode
├── NullNode
├── ListNode
├── DictNode
├── VariableAccessNode
├── AssignmentNode
├── BinaryOpNode
├── UnaryOpNode
├── IfNode
├── WhileNode
├── ForNode
├── FunctionDefNode
├── ReturnNode
├── CallNode
├── IndexAccessNode
├── SliceNode
├── PrintNode
├── InputNode
├── ShowNode
├── BreakNode
├── ContinueNode
├── ExitNode
├── ImportNode
├── TryNode
└── BlockNode
```

---

## 4. Evaluator (`evaluator.py`)

### Tugas
Mengeksekusi AST.

### Environment Chain

Setiap scope direpresentasikan oleh `Environment`:

```python
class Environment:
    variables: dict
    parent: Environment | None
```

- `get(name)` — mencari variabel dari scope saat ini hingga global.
- `set(name, value)` — mengubah variabel yang sudah ada, atau membuat di scope saat ini.
- `define(name, value)` — membuat variabel baru di scope ini (untuk parameter dan fungsi).

### Closure

Saat `FunctionDefNode` dievaluasi:

1. Node disalin dengan `copy.copy()`.
2. Atribut `closure` diisi dengan environment saat definisi.
3. Fungsi disimpan di environment.

Saat dipanggil, environment lokal dibuat dengan `parent = func.closure`, sehingga variabel dari lingkungan definisi tetap dapat diakses.

### Sinyal Kontrol

Evaluator menggunakan exception Python untuk sinyal kontrol:

| Exception | Dipicu oleh | Ditangani oleh |
|-----------|-------------|----------------|
| `ReturnSignal` | `balekken`/`muba` | Pemanggil fungsi (`eval_call`) |
| `BreakSignal` | `kajab` | Loop (`while`, `for`) |
| `ContinueSignal` | `lanjar` | Loop (`while`, `for`) |
| `ExitSignal` | `kaluar` | Top-level `run()` |

Pendekatan ini membuat kode evaluator bersih dan mudah dibaca.

### Error Handling

Jika exception terjadi saat evaluasi, `run()` menangkapnya dan menampilkan pesan dengan **baris dan kolom** dari node saat itu (`self.current_node`).

---

## 5. Alur Eksekusi Lengkap

```
1. main.py membaca file atau input REPL.
2. Lexer.tokenize() → daftar token.
3. Parser.parse() → BlockNode (root AST).
4. Evaluator.run(ast) → eksekusi.
5. Setiap node dievaluasi secara rekursif.
6. Output ditulis ke stdout.
```

---

## Referensi

- Nystrom, R. (2021). *Crafting Interpreters*. Genever Benning.
- Aho, A. V., et al. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.