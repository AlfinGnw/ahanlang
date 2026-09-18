<div align="center">

# AHAN

**Bahasa Pemrograman Imperatif dengan Sintaks Bahasa Devayan**

*Berkata lewat kode.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](#status-proyek)

</div>

---

## Daftar Isi

- [Tentang AHAN](#tentang-ahan)
- [Fitur Utama](#fitur-utama)
- [Arsitektur](#arsitektur)
- [Instalasi](#instalasi)
- [Penggunaan Cepat](#penggunaan-cepat)
- [Contoh Kode](#contoh-kode)
- [Dokumentasi](#dokumentasi)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Status Proyek](#status-proyek)
- [Berkontribusi](#berkontribusi)
- [Lisensi](#lisensi)

---

## Tentang AHAN

**AHAN** adalah bahasa pemrograman imperatif sumber terbuka yang menggabungkan kesederhanaan sintaks bergaya Python dengan kekayaan kosakata **bahasa Devayan** — bahasa asli masyarakat Pulau Simeulue, Aceh, Indonesia.

Nama **AHAN** diambil dari kata kunci utamanya, `ahan`, yang berarti *"mengucapkan"* atau *"berkata"*. Filosofinya sederhana: menulis program adalah cara **berkata** kepada komputer, dan `ahan` adalah perintah untuk menyampaikan sesuatu.

Proyek ini bertujuan untuk:

- **Edukasi** — menjadi media pembelajaran konsep *lexer*, *parser*, *evaluator*, dan desain bahasa pemrograman.
- **Pelestarian Budaya** — memperkenalkan bahasa Devayan ke ranah teknologi modern.
- **Eksperimen** — menjadi *playground* untuk ide-ide bahasa pemrograman yang unik.

> **Catatan**: AHAN saat ini berada dalam tahap **prototipe**. API dan sintaks dapat berubah sewaktu-waktu.

---

## Fitur Utama

| Kategori | Fitur |
|----------|-------|
| **Paradigma** | Imperatif, dengan dukungan closure |
| **Sintaks** | Indentasi (seperti Python), kata kunci Devayan |
| **Tipe Data** | Integer, Float, String, Boolean, Null, List, Dictionary |
| **Kontrol Alur** | `anga`/`laenne`, `salamo`, `mek`/`bak`, `kajab`, `lanjar` |
| **Fungsi** | `fungsi`, `balekken`/`muba`, closure, rekursi |
| **Modularitas** | Import file dengan `pakek` |
| **Error Handling** | `cubo`/`adorapek`, error dengan posisi baris/kolom |
| **List & Dict** | Indexing, slicing, modifikasi elemen |
| **I/O** | `ahan`/`kaluarken`, `baco`/`mitidao`, `antoroman` |
| **Operator** | Aritmetika, perbandingan, logika, assignment gabungan |

---

## Arsitektur

AHAN diimplementasikan sebagai **tree-walking interpreter** dengan tiga tahap klasik:

```
┌─────────────┐    ┌──────────┐    ┌─────────┐    ┌───────────┐
│ Source Code │───▶│  Lexer   │───▶│ Parser  │───▶│ Evaluator │
│   (.ahan)   │    │ (Tokens) │    │  (AST)  │    │  (Hasil)  │
└─────────────┘    └──────────┘    └─────────┘    └───────────┘
```

| File | Peran |
|------|-------|
| `token_types.py` | Konstanta jenis token |
| `lexer.py` | Tokenisasi kode sumber (indentasi, bracket, string, angka) |
| `ast_nodes.py` | Definisi node AST |
| `parser.py` | Pembangunan AST dari token (recursive descent) |
| `evaluator.py` | Eksekusi AST dengan environment chain |
| `main.py` | Entry point (REPL dan file runner) |

Detail lengkap ada di [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Instalasi

### Prasyarat

- **Python 3.8** atau lebih baru

### Langkah Instalasi

```bash
# 1. Clone repositori
git clone https://github.com/AlfinGnw/ahanlang.git
cd ahanlang

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Jalankan program pertama
python main.py examples/halo.ahan
```

Tidak ada dependensi eksternal — AHAN hanya menggunakan **Python Standard Library**.

---

## Penggunaan Cepat

### Menjalankan File

```bash
python main.py namafile.ahan
```

### Mode Interaktif (REPL)

```bash
python main.py
```

Contoh sesi REPL:

```
AHAN REPL v1.1
Ketik 'kaluar' atau Ctrl+D untuk keluar.
Untuk blok multi-baris, akhiri dengan baris kosong.

ahan> fungsi halo(nama):
   ...      ahan("Halo, " + nama)
   ...  
ahan> halo("Alfin")
Halo, Alfin
ahan> kaluar
```

---

## Contoh Kode

### 1. Program Hello World

```
nama = "Dunia"
ahan("Halo, " + nama + "!")
```

### 2. Fungsi Rekursif

```
fungsi faktorial(n):
    anga n <= 1:
        balekken 1
    laenne:
        balekken n * faktorial(n - 1)

ahan(faktorial(5))   # 120
```

### 3. Closure

```
fungsi pembuat_kali(faktor):
    fungsi kali(x):
        balekken x * faktor
    balekken kali

kali_dua = pembuat_kali(2)
ahan(kali_dua(10))   # 20
```

### 4. List dan Dictionary

```
daftar = [10, 20, 30]
daftar[0] = 100
ahan(daftar[1:3])    # [20, 30]

orang = {"nama": "Alfin", "umur": 25}
orang["umur"] += 1
ahan(orang["umur"])  # 26
```

### 5. Try/Except

```
cubo:
    hasil = 10 / 0
adorapek pesan:
    ahan("Error: " + pesan)
```

---

## Dokumentasi

| Dokumen | Deskripsi |
|---------|-----------|
| [docs/SYNTAX.md](docs/SYNTAX.md) | Panduan sintaks lengkap |
| [docs/KEYWORDS.md](docs/KEYWORDS.md) | Daftar lengkap kata kunci Devayan |
| [docs/STANDARD_LIBRARY.md](docs/STANDARD_LIBRARY.md) | Built-in function dan utilitas |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Detail arsitektur interpreter |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Rencana pengembangan |

---

## Teknologi yang Digunakan

### Bahasa Implementasi

| Teknologi | Versi | Peran |
|-----------|-------|-------|
| **Python** | 3.8+ | Bahasa utama implementasi interpreter |

### Konsep Ilmu Komputer

- **Lexical Analysis** — tokenisasi dengan *hand-written lexer*.
- **Recursive Descent Parsing** — parsing top-down untuk membangun AST.
- **Tree-Walking Interpreter** — evaluasi AST secara langsung.
- **Environment Chain** — scope variabel dengan linked environment untuk closure.
- **Exception-Based Control Flow** — exception Python untuk sinyal `return`, `break`, `continue`, `exit`.

### Standar Library Python

- `sys` — argumen command-line dan I/O.
- `os` — resolusi path untuk import modul.
- `copy` — penyalinan node untuk closure.

### Tidak Menggunakan

- Parser generator (ANTLR, Yacc, PLY) — agar konsep parsing dipahami sepenuhnya.
- LLVM atau backend kompilasi — fokus pada kesederhanaan.
- Framework web atau ORM — proyek ini murni interpreter.

---

## Status Proyek

| Aspek | Status |
|-------|--------|
| **Versi** | `0.1.0` (prototipe) |
| **Stabilitas API** | ❌ Belum stabil |
| **Cakupan Test** | ⚠️ Manual testing |
| **Dokumentasi** | ✅ Lengkap |
| **Distribusi PyPI** | ⏳ Direncanakan |
| **Web Playground** | ⏳ Direncanakan |

---

## Berkontribusi

Kontribusi sangat diterima — baik laporan bug, usulan fitur, perbaikan dokumentasi, maupun pull request.

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.

### Alur Cepat

1. **Fork** repositori.
2. Buat **branch** fitur: `git checkout -b fitur-keren`.
3. **Commit**: `git commit -m "feat: tambah fitur keren"`.
4. **Push**: `git push origin fitur-keren`.
5. Buka **Pull Request**.

---

## Lisensi

**MIT License** — lihat file [LICENSE](LICENSE).

---

## Ucapan Terima Kasih

- Masyarakat **Simeulue** atas warisan bahasa Devayan.
- Robert Nystrom atas buku *[Crafting Interpreters](https://craftinginterpreters.com/)*.
- Komunitas **Python Indonesia** atas inspirasi.

---

<div align="center">

**Dibuat dengan ❤️ untuk pelestarian bahasa dan edukasi teknologi.**

</div>