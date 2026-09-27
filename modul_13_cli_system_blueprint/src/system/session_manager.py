"""
src/system/session_manager.py
------------------------------
Pengelola status sesi aktif pengguna. Menyimpan kondisi sistem secara
persisten antar-eksekusi perintah (mis. perintah terakhir, waktu mulai,
jumlah eksekusi) ke dalam berkas JSON di data_dir.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict


class SessionManager:
    """Mengelola siklus hidup satu sesi CLI: start -> touch -> end."""

    def __init__(self, settings) -> None:
        self._settings = settings
        self._path: Path = settings.data_dir / settings.session_file_name
        self._state: Dict[str, Any] = {}

    def start(self) -> None:
        """Muat sesi lama jika masih valid (belum expired), atau buat baru."""
        self._settings.ensure_dirs()
        existing = self._read()

        if existing and self._is_valid(existing):
            self._state = existing
            self._state["resumed"] = True
        else:
            self._state = {
                "session_id": str(uuid.uuid4()),
                "created_at": time.time(),
                "resumed": False,
                "command_count": 0,
                "last_command": None,
            }

        self._state["last_started_at"] = time.time()
        self._write()

    def touch(self, command_name: str) -> None:
        """Catat bahwa sebuah command baru saja dieksekusi dalam sesi ini."""
        self._state["command_count"] = self._state.get("command_count", 0) + 1
        self._state["last_command"] = command_name
        self._state["updated_at"] = time.time()
        self._write()

    def end(self) -> None:
        """Tutup sesi dengan aman dan simpan state akhir ke disk."""
        self._state["ended_at"] = time.time()
        self._write()

    def _is_valid(self, state: Dict[str, Any]) -> bool:
        created_at = state.get("created_at", 0)
        age = time.time() - created_at
        return age < self._settings.session_ttl_seconds

    def _read(self) -> Dict[str, Any]:
        if not self._path.exists():
            return {}
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write(self) -> None:
        self._path.write_text(json.dumps(self._state, indent=2), encoding="utf-8")

    @property
    def state(self) -> Dict[str, Any]:
        return dict(self._state)
