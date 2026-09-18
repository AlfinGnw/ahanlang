# Sintaks AHAN

Panduan lengkap sintaks bahasa pemrograman **AHAN**.

## Daftar Isi

- [Komentar](#komentar)
- [Variabel](#variabel)
- [Tipe Data](#tipe-data)
- [Operator](#operator)
- [Percabangan](#percabangan)
- [Perulangan](#perulangan)
- [Fungsi](#fungsi)
- [List dan Dictionary](#list-dan-dictionary)
- [Input dan Output](#input-dan-output)
- [Try/Except](#tryexcept)
- [Import](#import)
- [Exit](#exit)
- [Konversi Tipe](#konversi-tipe)

---

## Komentar

```
# Ini komentar satu baris
ahan("Halo")   # komentar di akhir baris
```

## Variabel

Tidak ada kata kunci deklarasi — cukup assignment:

```
x = 10
nama = "Alfin"
aktif = dise
data = [1, 2, 3]
orang = {"nama": "Alfin", "umur": 25}
```

## Tipe Data

| Tipe | Contoh |
|------|--------|
| Integer | `10`, `-5`, `0` |
| Float | `3.14`, `2.0`, `-0.5` |
| String | `"halo"`, `'halo'` |
| Boolean | `dise` (true), `salah` (false) |
| Null | `kosong` |
| List | `[1, 2, 3]`, `["a", "b"]` |
| Dictionary | `{"kunci": "nilai"}` |

## Operator

### Aritmetika

| Operator | Deskripsi |
|----------|-----------|
| `+` | Penjumlahan / konkatenasi string |
| `-` | Pengurangan |
| `*` | Perkalian |
| `/` | Pembagian |
| `%` | Modulo |
| `^` | Pangkat |

### Perbandingan

`==`, `!=`, `<`, `>`, `<=`, `>=`

### Logika

| Kata Kunci | Padanan |
|------------|---------|
| `dan` | and |
| `atau` | or |
| `teen` | not |

### Assignment Gabungan

`+=`, `-=`, `*=`, `/=`, `%=`, `^=`

Contoh:

```
x = 10
x += 5      # x = 15
x *= 2      # x = 30
```

## Percabangan

```
anga x > 10:
    ahan("besar")
laenne anga x > 5:
    ahan("sedang")
laenne:
    ahan("kecil")
```

## Perulangan

### While (`salamo`)

```
i = 0
salamo i < 5:
    ahan(i)
    i += 1
```

### For (`mek ... bak ...`)

```
daftar = [1, 2, 3, 4, 5]
mek item bak daftar:
    ahan(item)
```

### Break dan Continue

```
mek i bak [1, 2, 3, 4, 5]:
    anga i == 3:
        lanjar       # lewati iterasi ini
    anga i == 5:
        kajab        # keluar dari loop
    ahan(i)
```

## Fungsi

### Deklarasi

```
fungsi tambah(a, b):
    balekken a + b

ahan(tambah(2, 3))   # 5
```

### Tanpa Return

```
fungsi sapa(nama):
    ahan("Halo, " + nama)

sapa("Alfin")
```

### Rekursi

```
fungsi faktorial(n):
    anga n <= 1:
        balekken 1
    laenne:
        balekken n * faktorial(n - 1)
```

### Closure

```
fungsi pembuat_kali(faktor):
    fungsi kali(x):
        balekken x * faktor
    balekken kali

kali_dua = pembuat_kali(2)
ahan(kali_dua(10))   # 20
```

## List dan Dictionary

### List

```
daftar = [10, 20, 30, 40]

ahan(daftar[0])        # 10
ahan(daftar[1:3])      # [20, 30]
ahan(daftar[2:])       # [30, 40]
ahan(daftar[:2])       # [10, 20]

daftar[0] = 100        # modifikasi elemen
daftar[1] += 5
ahan(panjang(daftar))  # 4
```

### Dictionary

```
orang = {
    "nama": "Alfin",
    "umur": 25,
    "kota": "Simeulue"
}

ahan(orang["nama"])    # Alfin
orang["umur"] += 1     # modifikasi nilai
orang["pekerjaan"] = "Programmer"   # tambah kunci baru

ahan(kunci(orang))     # ['nama', 'umur', 'kota', 'pekerjaan']
ahan(nilai(orang))     # ['Alfin', 26, 'Simeulue', 'Programmer']
ahan(pasangan(orang))  # [['nama', 'Alfin'], ...]
```

## Input dan Output

### Output

```
ahan("Halo")              # cetak + newline
kaluarken("Halo")         # alias
antoroman("Halo ")        # cetak tanpa newline
antoroman("Dunia")        # lanjut di baris yang sama
ahan("")                  # pindah baris
```

### Input

```
nama = baco("Nama: ")
umur = mitidao("Umur: ")
```

## Try/Except

```
cubo:
    hasil = 10 / 0
adorapek pesan:
    ahan("Error: " + pesan)
```

Tanpa variabel error:

```
cubo:
    x = int("abc")
adorapek:
    ahan("Input tidak valid")
```

## Import

```
pakek "modul_saya"
pakek modul_saya
```

File yang diimpor harus berekstensi `.ahan`. Ekstensi ditambahkan otomatis jika tidak ada.

## Exit

```
anga kondisi:
    ahan("Keluar...")
    kaluar
```

## Konversi Tipe

```
a = int("42")       # 42
b = float("3.14")   # 3.14
c = str(42)         # "42"
```

## Utilitas Built-in

| Fungsi | Deskripsi |
|--------|-----------|
| `panjang(x)` | Panjang list atau string |
| `abek(x, i, default)` | Ambil elemen dengan aman |
| `kunci(d)` | Daftar kunci dictionary |
| `nilai(d)` | Daftar nilai dictionary |
| `pasangan(d)` | Daftar pasangan [kunci, nilai] |

Lihat [STANDARD_LIBRARY.md](STANDARD_LIBRARY.md) untuk detail.