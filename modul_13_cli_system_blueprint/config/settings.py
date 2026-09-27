"""
config/settings.py
-------------------
Environment config loader (.env & system variables).
Memuat seluruh nilai konfigurasi global yang dipakai lintas layer,
agar tidak ada nilai hardcoded tersembunyi di dalam kode bisnis.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

# Lokasi root project (dua tingkat di atas file ini: config/ -> root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Mencoba memuat file .env sederhana (tanpa dependensi eksternal python-dotenv)
def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Settings:
    """Objek konfigurasi immutable, dibaca sekali di awal siklus hidup app."""

    app_name: str = os.environ.get("APP_NAME", "cli-system-blueprint")
    app_version: str = os.environ.get("APP_VERSION", "1.0.0")
    debug: bool = field(default_factory=lambda: _get_bool("DEBUG", False))

    # Direktori data & storage
    data_dir: Path = field(default_factory=lambda: BASE_DIR / os.environ.get("DATA_DIR", "data"))

    # Session
    session_file_name: str = os.environ.get("SESSION_FILE", "session_state.json")
    session_ttl_seconds: int = int(os.environ.get("SESSION_TTL_SECONDS", "86400"))

    # Cache
    cache_max_items: int = int(os.environ.get("CACHE_MAX_ITEMS", "256"))

    # Shutdown
    shutdown_grace_period: float = float(os.environ.get("SHUTDOWN_GRACE_PERIOD", "2.0"))

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
