# User Manual
### CLI Project Defense Suite v1.0.0

Panduan penggunaan aplikasi secara menyeluruh.

## 1. Instalasi

```bash
pip install -e .
```

Atau via Docker (lihat `deploy/Dockerfile`):

```bash
make -C deploy docker-build
make -C deploy run-docker
```

## 2. Menjalankan Aplikasi

```bash
python main.py --help
```

Menampilkan splash screen dan dashboard ringkasan fitur:

```bash
python main.py --version
python main.py dashboard
```

## 3. Menjalankan Demo Sidang

Skenario singkat (4 langkah):

```bash
python main.py demo --scenario quick_tour
```

Skenario lengkap A-Z (untuk sesi sidang penuh):

```bash
python main.py demo --scenario full_defense
```

## 4. Membangun Executable Mandiri

```bash
python main.py build --target executable
```

Ini akan memanggil `src/packager/pyinstaller_build.py` dan menghasilkan
berkas biner di folder `dist/`.

## 5. Membangun Docker Image

```bash
python main.py build --target docker
```

## 6. Menghasilkan Dokumentasi & Slide Otomatis

```bash
python main.py docs generate
python main.py docs slides
```

## 7. Menjalankan Test

```bash
python -m pytest tests/ -v
```

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `pyinstaller: command not found` | Jalankan `pip install pyinstaller` |
| `docker: command not found` | Pastikan Docker Desktop/Engine terpasang & PATH benar |
| Demo terhenti mendadak | Cek `config/demo_scenarios.py` untuk memastikan skenario valid |
