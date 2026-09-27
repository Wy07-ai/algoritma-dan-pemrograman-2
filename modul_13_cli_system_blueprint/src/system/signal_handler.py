"""
src/system/signal_handler.py
------------------------------
Penanganan sinyal sistem operasi (SIGINT/Ctrl+C, SIGTERM) untuk memastikan
proses penulisan data diselesaikan terlebih dahulu sebelum aplikasi ditutup
(Graceful Shutdown), bukan langsung mati mendadak (abrupt kill).
"""

from __future__ import annotations

import signal
import sys
from typing import Callable


class SignalHandler:
    """Membungkus registrasi signal OS agar shutdown selalu lewat satu jalur."""

    def __init__(self, on_shutdown: Callable[[], None]) -> None:
        self._on_shutdown = on_shutdown
        self._triggered = False

    def install(self) -> None:
        signal.signal(signal.SIGINT, self._handle)
        try:
            signal.signal(signal.SIGTERM, self._handle)
        except (AttributeError, ValueError):
            # SIGTERM tidak selalu tersedia di semua platform (mis. Windows).
            pass

    def _handle(self, signum, frame) -> None:  # noqa: ARG002 - signature wajib OS
        if self._triggered:
            # Sinyal kedua kali: paksa keluar agar user tidak terjebak.
            sys.exit(1)

        self._triggered = True
        print("\n[signal] Sinyal interupsi diterima, menutup aplikasi dengan aman...")
        self._on_shutdown()
        sys.exit(0)
