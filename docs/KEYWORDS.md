# Daftar Kata Kunci AHAN

Semua kata kunci dalam AHAN menggunakan kosakata **bahasa Devayan** (Simeulue, Aceh). Kata kunci bersifat **case-sensitive** dan ditulis dalam huruf kecil.

## Kategori

### Kontrol Alur

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `anga` | if | Percabangan kondisional |
| `laenne` | else | Cabang alternatif |
| `laenne anga` | else if | Percabangan berantai |
| `salamo` | while | Perulangan selama kondisi benar |
| `mek` | for | Perulangan iteratif |
| `bak` | in | Kata penghubung iterasi |
| `kajab` | break | Keluar dari loop |
| `lanjar` | continue | Lompat ke iterasi berikutnya |
| `kaluar` | exit | Keluar dari program |

### Fungsi

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `fungsi` | function | Deklarasi fungsi |
| `balekken` | return | Mengembalikan nilai dari fungsi |
| `muba` | return | Alias dari `balekken` |

### Input/Output

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `ahan` | print | Cetak dengan newline — **kata kunci utama** |
| `kaluarken` | print | Alias dari `ahan` |
| `antoroman` | show | Cetak tanpa newline |
| `baco` | input | Baca input dari pengguna |
| `mitidao` | input | Alias dari `baco` |

### Tipe dan Nilai

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `dise` | true | Nilai boolean benar |
| `salah` | false | Nilai boolean salah |
| `kosong` | null | Nilai kosong |

### Operator Logika

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `dan` | and | Konjungsi logika |
| `atau` | or | Disjungsi logika |
| `teen` | not | Negasi logika |

### Modul dan Error

| Kata Kunci | Padanan | Deskripsi |
|------------|---------|-----------|
| `pakek` | import | Impor file AHAN |
| `cubo` | try | Blok percobaan |
| `adorapek` | catch | Blok penanganan error |

---

## Daftar Lengkap (Alfabetis)

```
adorapek    → catch
ahan        → print (kata kunci utama)
anga        → if
antoroman   → show (tanpa newline)
atau        → or
bak         → in (untuk for)
baco        → input
balekken    → return
cubo        → try
dan         → and
dise        → true
fungsi      → function
kajab       → break
kaluar      → exit
kaluarken   → print (alias)
kosong      → null
laenne      → else
lanjar      → continue
mek         → for
mitidao     → input (alias)
muba        → return (alias)
pakek       → import
salah       → false
salamo      → while
teen        → not
```

---

## Alias

AHAN menyediakan alias agar pengguna dapat memilih istilah yang paling nyaman:

| Fungsi | Utama | Alias |
|--------|-------|-------|
| Output | `ahan` | `kaluarken` |
| Input | `baco` | `mitidao` |
| Return | `balekken` | `muba` |

> **Catatan**: `ahan` dijadikan kata kunci utama karena menjadi identitas bahasa. `kaluarken` tetap didukung sebagai alias untuk kompatibilitas.