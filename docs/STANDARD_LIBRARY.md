# Standard Library AHAN

AHAN menyediakan sekumpulan **built-in function** yang dapat digunakan tanpa import.

## Konversi Tipe

### `int(x)`

Mengonversi nilai menjadi integer.

```
a = int("42")       # 42
b = int(3.14)       # 3
```

Jika nilai tidak dapat dikonversi, akan terjadi error yang bisa ditangkap dengan `cubo`.

### `float(x)`

Mengonversi nilai menjadi float.

```
a = float("3.14")   # 3.14
b = float(5)        # 5.0
```

### `str(x)`

Mengonversi nilai menjadi string.

```
a = str(42)         # "42"
b = str(3.14)       # "3.14"
```

---

## Utilitas List dan String

### `panjang(x)`

Mengembalikan panjang list atau string.

```
panjang([1, 2, 3])         # 3
panjang("Simeulue")        # 8
panjang({"a": 1, "b": 2})  # 2 (jumlah kunci)
```

### `abek(container, index, default=kosong)`

Mengambil elemen dengan aman. Jika indeks tidak valid, mengembalikan `default`.

```
daftar = [10, 20, 30]
abek(daftar, 0)             # 10
abek(daftar, 10)            # kosong
abek(daftar, 10, "N/A")     # "N/A"
```

---

## Utilitas Dictionary

### `kunci(d)`

Mengembalikan daftar kunci dari dictionary.

```
orang = {"nama": "Alfin", "umur": 25}
kunci(orang)   # ["nama", "umur"]
```

### `nilai(d)`

Mengembalikan daftar nilai dari dictionary.

```
nilai(orang)   # ["Alfin", 25]
```

### `pasangan(d)`

Mengembalikan daftar pasangan `[kunci, nilai]`.

```
pasangan(orang)   # [["nama", "Alfin"], ["umur", 25]]
```

---

## Output dan Input

### `ahan(x)` / `kaluarken(x)`

Mencetak nilai diikuti newline.

```
ahan("Halo, Dunia!")
ahan(42)
ahan([1, 2, 3])
```

### `antoroman(x)`

Mencetak nilai tanpa newline.

```
antoroman("Nama: ")
ahan("Alfin")
# Output: Nama: Alfin
```

### `baco(prompt)` / `mitidao(prompt)`

Membaca input dari pengguna dengan prompt opsional.

```
nama = baco("Nama Anda: ")
ahan("Halo, " + nama)
```

---

## Operator Indexing

List, string, dan dictionary mendukung operator `[]`:

### List

```
daftar = [10, 20, 30, 40]
daftar[0]           # 10
daftar[1:3]         # [20, 30]
daftar[2:]          # [30, 40]
daftar[:2]          # [10, 20]
daftar[-1]          # 40 (indeks negatif didukung, dari akhir)
```

### String

```
teks = "Simeulue"
teks[0]             # "S"
teks[0:4]           # "Sime"
teks[-1]            # "e" (indeks dari akhir)
```

### Dictionary

```
orang = {"nama": "Alfin", "umur": 25}
orang["nama"]       # "Alfin"
orang["umur"] = 26  # modifikasi
orang["kota"] = "Simeulue"  # tambah kunci
```

---

## Ringkasan Built-in

| Fungsi | Deskripsi |
|--------|-----------|
| `int(x)` | Konversi ke integer |
| `float(x)` | Konversi ke float |
| `str(x)` | Konversi ke string |
| `panjang(x)` | Panjang list/string/dict |
| `abek(c, i, def)` | Ambil elemen dengan aman |
| `kunci(d)` | Kunci dictionary |
| `nilai(d)` | Nilai dictionary |
| `pasangan(d)` | Pasangan kunci-nilai |
| `ahan(x)` | Cetak dengan newline |
| `kaluarken(x)` | Alias `ahan` |
| `antoroman(x)` | Cetak tanpa newline |
| `baco(p)` | Baca input |
| `mitidao(p)` | Alias `baco` |