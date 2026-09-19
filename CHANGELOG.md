# Changelog

Semua perubahan penting pada proyek ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Ditambahkan
- **Ekstensi VS Code** untuk syntax highlighting AHAN (`vscode-ahan/`) — grammar TextMate, language-configuration, dan snippets
- **Test suite otomatis** dengan pytest (`tests/`) — 86 test untuk lexer, parser, dan evaluator

### Diperbaiki
- Angka desimal yang diawali titik (`x = .5`) kini dikenali sebagai float
- Operator pangkat (`^`) kini bersifat right-associative: `2 ^ 3 ^ 2` = 512
- Target assignment invalid (`1 + 2 = 5`) ditolak saat parsing dengan pesan jelas
- Postfix indexing kini berlaku pada semua ekspresi primary (string literal, list literal, hasil pemanggilan, ekspresi dalam kurung)
- Indeks negatif didukung untuk list dan string: `daftar[-1]`
- Output boolean/nil konsisten: `dise`, `salah`, `kosong`
- Error fase lexer/parse diformat rapi dengan nomor baris dan kolom
- `run_file()` mendukung deteksi encoding otomatis (UTF-8, UTF-16, latin-1)

### Direncanakan

## [0.1.0] - 2025-01-XX

### Ditambahkan
- **Interpreter AHAN** (sebelumnya SimeulueLang) — prototipe awal
- **Lexer** dengan dukungan indentasi, bracket tracking, string escape
- **Parser** recursive descent dengan preseden operator lengkap
- **Evaluator** tree-walking dengan environment chain untuk closure
- **Kata kunci Devayan**: `anga`, `laenne`, `salamo`, `mek`, `bak`, `kajab`, `lanjar`, `fungsi`, `balekken`/`muba`, `ahan`/`kaluarken`, `baco`/`mitidao`, `antoroman`, `kaluar`, `pakek`, `cubo`, `adorapek`, `dise`, `salah`, `kosong`, `dan`, `atau`, `teen`
- **Tipe data**: integer, float, string, boolean, null, list, dictionary
- **Kontrol alur**: if/else, while, for-list, break, continue
- **Fungsi** dengan closure dan rekursi
- **Import modular** (`pakek`)
- **Try/except** (`cubo`/`adorapek`)
- **I/O**: `ahan`, `kaluarken`, `baco`, `mitidao`, `antoroman`
- **Exit program** (`kaluar`)
- **Operator gabungan** (`+=`, `-=`, `*=`, `/=`, `%=`, `^=`)
- **Indexing dan slicing** untuk list, string, dictionary
- **Modifikasi elemen** list dan dictionary
- **Error handling** dengan posisi baris/kolom
- **REPL interaktif** dengan auto-indentasi
- **Built-in functions**: `int`, `float`, `str`, `panjang`, `abek`, `kunci`, `nilai`, `pasangan`
- **Contoh program**: halo, faktorial, fibonacci, kalkulator modular
- **Dokumentasi lengkap**: README, arsitektur, sintaks, kata kunci, standard library

### Catatan
- Versi awal, API belum stabil.
- Belum dipublikasikan ke PyPI.