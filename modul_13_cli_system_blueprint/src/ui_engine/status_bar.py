"""
src/ui_engine/status_bar.py
------------------------------
Menampilkan status baris sistem (status bar) di bagian bawah terminal:
nama sesi, jumlah command yang sudah dieksekusi, dan versi aplikasi.
"""

from __future__ import annotations

from typing import Any, Dict


class StatusBar:
    """Merender satu baris ringkasan status sistem untuk ditampilkan tiap saat."""

    def __init__(self, app_name: str, app_version: str) -> None:
        self._app_name = app_name
        self._app_version = app_version

    def render(self, session_state: Dict[str, Any]) -> str:
        session_id = str(session_state.get("session_id", "-"))[:8]
        count = session_state.get("command_count", 0)
        resumed = "resumed" if session_state.get("resumed") else "new"

        return (
            f"[{self._app_name} v{self._app_version}] "
            f"session={session_id} ({resumed}) | perintah dijalankan: {count}"
        )
