# Roadmap AHAN

Dokumen ini menjelaskan rencana pengembangan AHAN ke depan.

## Status: `v0.1.0` (Prototype)

Versi saat ini sudah berfungsi sebagai bahasa pemrograman dasar dengan fitur lengkap untuk pemrograman umum. Fokus saat ini adalah **stabilitas**, **distribusi**, dan **dokumentasi**.

---

## v0.2.0 — Stabilisasi

**Target**: Tahap 1

- [ ] Test suite otomatis dengan `pytest`
- [ ] Refactor kode untuk kejelasan
- [ ] Dokumentasi API internal (docstring)
- [ ] Perbaikan bug hasil uji komunitas
- [ ] Contoh program tambahan

---

## v0.3.0 — Distribusi

**Target**: Tahap 2

- [ ] Publikasi ke **PyPI** sebagai `ahanlang`
- [ ] Instalasi via `pip install ahanlang`
- [ ] Executable mandiri dengan **PyInstaller**
- [ ] Docker image resmi
- [ ] Extension **VS Code** untuk syntax highlighting

---

## v0.4.0 — Web Playground

**Target**: Tahap 3

- [ ] Web REPL menggunakan **Pyodide** (Python di browser)
- [ ] Editor kode dengan **CodeMirror** atau **Monaco**
- [ ] Deployment ke **GitHub Pages**
- [ ] Dokumentasi interaktif

---

## v0.5.0 — Fitur Bahasa Lanjutan

**Target**: Tahap 4

- [ ] Kelas dan objek (`kelas`, `ini`)
- [ ] Modul sistem yang lebih baik (`pakek` dari paket)
- [ ] Metode string bawaan (`ganti`, `pecah`, `gabung`)
- [ ] List comprehension
- [ ] Generator / iterator

---

## v1.0.0 — Stabil

**Target**: Tahap 5

- [ ] API stabil
- [ ] Dokumentasi lengkap dan final
- [ ] Komunitas aktif
- [ ] Ekosistem paket pihak ketiga

---

## Ide Jangka Panjang

- **Kompilasi ke bytecode** — untuk performa.
- **Backend LLVM** — untuk kompilasi native.
- **Interoperabilitas Python** — memanggil library Python dari AHAN.
- **Package manager** — seperti `pip` untuk AHAN.
- **Bahasa Devayan yang lebih kaya** — bekerja sama dengan ahli bahasa untuk memperluas kosakata.
- **Standard library resmi** — koleksi modul standar.

---

## Kontribusi

Ingin membantu mewujudkan salah satu item di roadmap? Buka issue atau hubungi maintainer di [GitHub Discussions](https://github.com/AlfinGnw/ahanlang/discussions).