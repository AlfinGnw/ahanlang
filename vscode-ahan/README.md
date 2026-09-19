# AHAN Language — Ekstensi VS Code

Syntax highlighting untuk bahasa pemrograman **AHAN** (SimeulueLang) — bahasa imperatif dengan sintaks bahasa Devayan dari Pulau Simeulue, Aceh.

## Fitur

- Highlight kata kunci (keyword) AHAN
- String, angka, komentar dengan warna yang berbeda
- Pemanggilan fungsi dan deklarasi fungsi (`fungsi`)
- Operator aritmetika, perbandingan, dan logika
- Auto-closing kurung/kutip, auto-indentasi untuk blok bertitik-dua (`:`)
- Snippets untuk konstruksi umum (`anga`, `salamo`, `mek`, `fungsi`, `kaluarken`, `baco`)

## Cara Instalasi

Jalankan dengan **F5** (dari folder ini) atau kemas menjadi `.vsix`:

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension ahan-language-0.1.0.vsix
```

Atau salin folder ini ke `~/.vscode/extensions/ahanlang.ahan-language-0.1.0`.

## Bahasa

File dengan ekstensi `.ahan` otomatis dikenali. Referensi bahasa: [`docs/`](../docs/), contoh program: [`examples/`](../examples/).

## Development

Struktur:

```
vscode-ahan/
├── package.json                  # manifest ekstensi
├── language-configuration.json   # komentar, bracket, indentasi
├── syntaxes/
│   └── ahan.tmLanguage.json      # grammar TextMate (source.ahan)
└── snippets/
    └── ahan.json                 # snippets
```