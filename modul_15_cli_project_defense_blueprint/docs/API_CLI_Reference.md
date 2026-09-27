# API / CLI Reference
### Referensi argumen & flag CLI — `main.py`

> Bagian ini dapat diregenerasi otomatis dengan menjalankan
> `python main.py --help` dan subperintahnya; ringkasan di bawah
> disediakan sebagai referensi statis untuk dokumentasi sidang.

## Perintah Global

| Flag | Deskripsi |
|---|---|
| `--version` | Menampilkan splash screen ASCII art beserta metadata rilis (versi, build date, author). |

## Subperintah: `dashboard`

```bash
python main.py dashboard
```
Menampilkan **Defense Dashboard** — tabel ringkasan fitur, tingkat kompleksitas Big-O per modul, dan status kesiapan sistem.

## Subperintah: `demo`

```bash
python main.py demo --scenario <quick_tour|full_defense> [--speed 0.02]
```

| Argumen | Wajib | Default | Deskripsi |
|---|---|---|---|
| `--scenario` | Tidak | `quick_tour` | Nama skenario dari `config/demo_scenarios.py` |
| `--speed` | Tidak | `0.02` | Kecepatan simulasi ketik (detik per karakter) |

## Subperintah: `build`

```bash
python main.py build --target <executable|docker> [--dry-run]
```

| Argumen | Wajib | Deskripsi |
|---|---|---|
| `--target` | Ya | `executable` (PyInstaller) atau `docker` (Docker image) |
| `--dry-run` | Tidak (default aktif) | Hanya menampilkan perintah build tanpa mengeksekusi |

## Subperintah: `docs`

```bash
python main.py docs generate   # Ekstrak docstring -> docs/GENERATED_CODE_DOCS.md
python main.py docs slides     # Cetak slide deck ringkasan audit ke stdout
```

## Kode Keluar (Exit Codes)

| Kode | Arti |
|---|---|
| `0` | Sukses |
| `1` | Kesalahan umum (lihat pesan error) |
| `130` | Dihentikan pengguna via Ctrl+C (SIGINT) |
