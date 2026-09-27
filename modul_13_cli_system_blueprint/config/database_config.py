"""
config/database_config.py
--------------------------
Konfigurasi koneksi penyimpanan lokal (SQLite) yang dipakai oleh
src/storage/local_db.py. Terpisah dari settings.py agar parameter
storage bisa berkembang sendiri (mis. ganti ke Postgres) tanpa
menyentuh konfigurasi aplikasi umum.
"""

from dataclasses import dataclass
from pathlib import Path

from config.settings import settings


@dataclass(frozen=True)
class DatabaseConfig:
    driver: str = "sqlite"
    db_path: Path = settings.data_dir / "local_store.db"
    timeout_seconds: float = 5.0
    check_same_thread: bool = False

    def ensure_ready(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)


database_config = DatabaseConfig()
