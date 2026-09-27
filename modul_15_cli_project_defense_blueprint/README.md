# Modul 15 — CLI Project Defense Blueprint

Fase akhir pengembangan aplikasi: **Pengemasan Rilis (Release Packaging)**,
**Reproduksibilitas Environment**, dan **Otomatisasi Presentasi Proyek**
(Project Defense).

Proyek ini mengemas sistem yang telah diaudit di Modul 14 ke dalam bentuk
Executable Binary atau Container, dilengkapi dokumentasi standar industri,
serta skenario demonstrasi otomatis untuk menjamin kelancaran sidang.

## Struktur Folder

```
modul_15_cli_project_defense_blueprint/
├── config/                 # Metadata rilis & skenario demo
├── docs/                   # ADR, User Manual, API/CLI Reference
├── src/
│   ├── packager/            # PyInstaller & Docker build automation
│   ├── generator/           # Doc generator & slide deck builder
│   ├── simulator/           # Auto typer & scenario runner (anti-gagal sidang)
│   └── ui/                  # Splash screen & defense dashboard
├── tests/                   # Pre-release verification suite
├── deploy/                  # Dockerfile & Makefile
├── main.py                  # Entry point (Defense Runner)
├── pyproject.toml
└── .env.example
```

## Quickstart

```bash
pip install -e .
python main.py --version
python main.py dashboard
python main.py demo --scenario quick_tour
python -m pytest tests/ -v
```

Lihat `docs/User_Manual.md` untuk panduan lengkap dan
`docs/API_CLI_Reference.md` untuk referensi seluruh perintah.
