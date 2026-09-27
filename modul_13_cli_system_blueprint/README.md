# Modul 13 — CLI System Blueprint

Sistem internal aplikasi CLI secara menyeluruh (Full-Stack CLI System):
bootstrapping sistem, pengelola status sesi, abstraksi penyimpanan lokal,
dan penanganan sinyal OS untuk penutupan aplikasi yang aman.

Lihat `docs/system_architecture.md` dan `docs/state_lifecycle.md` untuk
penjelasan arsitektur lengkap.

## Instalasi

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"          # opsional, untuk pytest
cp .env.example .env             # sesuaikan bila perlu
```

Tidak ada dependensi eksternal wajib — seluruh fungsi memakai pustaka
standar Python (`sqlite3`, `json`, `argparse`, `signal`).

## Penggunaan CLI

```bash
python main.py add "Beli buku" --desc "Untuk kuliah Algo2"
python main.py list
python main.py get 1
python main.py update 1 --name "Beli buku baru"
python main.py delete 1
python main.py export --format json --out data/export.json
python main.py sync
python main.py status
```

Tekan `Ctrl+C` kapan pun saat aplikasi berjalan untuk menguji mekanisme
*graceful shutdown* — data yang sudah masuk akan tetap tersimpan aman.

## Menjalankan Test

```bash
pip install pytest
pytest
```

Mencakup:
- `tests/test_system_lifecycle.py` — boot & shutdown Kernel
- `tests/test_storage_persistence.py` — integritas simpan-baca data lokal
- `tests/test_signal_interruption.py` — penanganan sinyal Ctrl+C

## Struktur Proyek

```
modul_13_cli_system_blueprint/
├── config/
│   ├── settings.py            # Environment config loader
│   └── database_config.py     # Konfigurasi koneksi storage lokal
├── docs/
│   ├── system_architecture.md
│   └── state_lifecycle.md
├── src/
│   ├── system/
│   │   ├── kernel.py           # Bootstrapper utama
│   │   ├── session_manager.py  # Pengelola status sesi
│   │   └── signal_handler.py   # Graceful shutdown (Ctrl+C/SIGINT)
│   ├── storage/
│   │   ├── repository.py       # Repository Pattern
│   │   ├── local_db.py         # SQLite handler
│   │   └── cache_store.py      # In-memory LRU cache
│   ├── services/
│   │   ├── data_service.py
│   │   ├── export_service.py
│   │   └── sync_service.py
│   └── ui_engine/
│       ├── view_router.py
│       └── status_bar.py
├── tests/
├── .env.example
├── main.py
├── pyproject.toml
└── README.md
```
