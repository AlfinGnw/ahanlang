# Panduan Kontribusi AHAN

Terima kasih atas minat Anda untuk berkontribusi pada **AHAN**!

## Cara Berkontribusi

### Melaporkan Bug

1. Cek dulu [Issues](https://github.com/AlfinGnw/ahanlang/issues) — mungkin bug sudah dilaporkan.
2. Jika belum, buat issue baru dengan judul deskriptif.
3. Sertakan:
   - Versi Python yang digunakan
   - Sistem operasi
   - Langkah reproduksi
   - Kode `.ahan` yang bermasalah
   - Pesan error lengkap

### Mengusulkan Fitur

1. Buat issue dengan label `enhancement`.
2. Jelaskan **mengapa** fitur ini penting, bukan hanya **apa**.
3. Berikan contoh sintaks yang diusulkan jika relevan.

### Pull Request

1. Fork repositori dan buat branch baru:
   ```bash
   git checkout -b fitur/nama-fitur
   ```
2. Ikuti gaya kode yang ada.
3. Tambahkan test jika memungkinkan.
4. Perbarui dokumentasi jika perlu.
5. Pastikan semua test lama masih lulus.
6. Buat pull request dengan deskripsi yang jelas.

## Gaya Kode

### Python

- Ikuti **PEP 8**.
- Indentasi **4 spasi**.
- Nama variabel dan fungsi: `snake_case`.
- Nama kelas: `PascalCase`.
- Komentar dalam bahasa Indonesia atau Inggris (konsisten dalam satu file).

### AHAN

- Kata kunci selalu **lowercase**.
- Indentasi **4 spasi**.
- Satu pernyataan per baris.

## Struktur Komit

Format pesan komit yang disarankan:

```
<tipe>: <deskripsi singkat>

<penjelasan opsional>
```

Tipe: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Contoh:

```
feat: tambah dukungan dictionary multi-baris

Parser sekarang mengabaikan newline di dalam bracket,
sehingga dict dapat ditulis dalam beberapa baris.
```

## Kode Etik

- Bersikap sopan dan inklusif.
- Kritik ide, bukan orang.
- Bantu kontributor baru.

## Pertanyaan?

Buka diskusi di [GitHub Discussions](https://github.com/AlfinGnw/ahanlang/discussions) atau hubungi maintainer.