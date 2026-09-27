"""
src/storage/local_db.py
-------------------------
Pengelola penyimpanan data lokal berbasis SQLite. Entitas disimpan dalam
satu tabel generik `entities` (entity_type + JSON payload) supaya
Repository tidak perlu skema tabel terpisah untuk tiap jenis data.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, List, Optional

from config.database_config import DatabaseConfig


class LocalDB:
    """Wrapper tipis di atas sqlite3 khusus untuk skema entities generik."""

    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self._config.ensure_ready()
        self._conn = sqlite3.connect(
            str(self._config.db_path),
            timeout=self._config.timeout_seconds,
            check_same_thread=self._config.check_same_thread,
        )
        self._conn.row_factory = sqlite3.Row

    def migrate(self) -> None:
        """Buat skema tabel jika belum ada (idempotent)."""
        assert self._conn is not None
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._conn.commit()

    def insert(self, entity_type: str, payload: Dict[str, Any]) -> int:
        assert self._conn is not None
        cur = self._conn.execute(
            "INSERT INTO entities (entity_type, payload) VALUES (?, ?)",
            (entity_type, json.dumps(payload)),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def find_by_id(self, entity_type: str, entity_id: int) -> Optional[Dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute(
            "SELECT id, payload, created_at FROM entities WHERE id = ? AND entity_type = ?",
            (entity_id, entity_type),
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def find_all(self, entity_type: str) -> List[Dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT id, payload, created_at FROM entities WHERE entity_type = ? ORDER BY id",
            (entity_type,),
        ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def update(self, entity_type: str, entity_id: int, payload: Dict[str, Any]) -> bool:
        assert self._conn is not None
        cur = self._conn.execute(
            "UPDATE entities SET payload = ? WHERE id = ? AND entity_type = ?",
            (json.dumps(payload), entity_id, entity_type),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def delete(self, entity_type: str, entity_id: int) -> bool:
        assert self._conn is not None
        cur = self._conn.execute(
            "DELETE FROM entities WHERE id = ? AND entity_type = ?",
            (entity_id, entity_type),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def commit(self) -> None:
        if self._conn is not None:
            self._conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        data = json.loads(row["payload"])
        data["id"] = row["id"]
        data["created_at"] = row["created_at"]
        return data
