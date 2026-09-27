"""
src/system/kernel.py
---------------------
Bootstrapper dan pengatur utama siklus hidup aplikasi (Init -> Run -> Terminate).
Kernel bertugas:
  1. Memuat konfigurasi (config/settings.py, config/database_config.py)
  2. Menginisialisasi dependensi (repository, session manager, cache)
  3. Menyiapkan signal handler untuk graceful shutdown
  4. Menyediakan konteks bersama ke seluruh command yang dieksekusi
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from config.database_config import database_config
from config.settings import settings
from src.storage.cache_store import CacheStore
from src.storage.local_db import LocalDB
from src.storage.repository import Repository
from src.system.session_manager import SessionManager
from src.system.signal_handler import SignalHandler

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="[%(levelname)s] %(name)s: %(message)s",
)


@dataclass
class AppContext:
    """Wadah dependensi yang dibawa ke seluruh command handler."""

    repository: Repository
    session: SessionManager
    cache: CacheStore


class Kernel:
    """Titik masuk tunggal untuk boot dan shutdown seluruh sistem."""

    def __init__(self) -> None:
        self.logger = logging.getLogger("kernel")
        self.context: AppContext | None = None
        self._signal_handler = SignalHandler(on_shutdown=self.shutdown)

    def boot(self) -> AppContext:
        """Tahap INIT: siapkan storage, session, cache, dan signal trap."""
        self.logger.debug("Booting %s v%s", settings.app_name, settings.app_version)

        settings.ensure_dirs()
        database_config.ensure_ready()

        local_db = LocalDB(database_config)
        local_db.connect()
        local_db.migrate()

        repository = Repository(local_db)
        cache = CacheStore(max_items=settings.cache_max_items)
        session = SessionManager(settings)
        session.start()

        self.context = AppContext(repository=repository, session=session, cache=cache)

        # Pasang signal handler (SIGINT / SIGTERM) untuk graceful shutdown.
        self._signal_handler.install()

        self.logger.info("Kernel siap. Sistem berada pada state: RUN")
        return self.context

    def shutdown(self) -> None:
        """Tahap TERMINATE: pastikan semua data tersimpan sebelum keluar."""
        if self.context is None:
            return

        self.logger.info("Menerima sinyal shutdown, menyelesaikan proses tulis data...")
        try:
            self.context.session.end()
            self.context.repository.flush()
            self.context.cache.clear()
        finally:
            self.logger.info("Shutdown selesai. Sistem berada pada state: TERMINATED")
            self.context = None
