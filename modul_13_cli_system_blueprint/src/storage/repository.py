"""
src/storage/repository.py
---------------------------
Penerapan Repository Pattern sebagai abstraksi tempat penyimpanan data,
memisahkan logika bisnis (src/services/) dari mekanisme basis data fisik
(src/storage/local_db.py). Service layer TIDAK boleh tahu ini SQLite atau
JSON - cukup panggil method repository.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.storage.local_db import LocalDB


class Repository:
    """Antarmuka CRUD generik di atas LocalDB, dipakai oleh service layer."""

    def __init__(self, db: LocalDB) -> None:
        self._db = db
        self._dirty = False

    def add(self, entity_type: str, payload: Dict[str, Any]) -> int:
        entity_id = self._db.insert(entity_type, payload)
        self._dirty = True
        return entity_id

    def get(self, entity_type: str, entity_id: int) -> Optional[Dict[str, Any]]:
        return self._db.find_by_id(entity_type, entity_id)

    def list_all(self, entity_type: str) -> List[Dict[str, Any]]:
        return self._db.find_all(entity_type)

    def update(self, entity_type: str, entity_id: int, payload: Dict[str, Any]) -> bool:
        ok = self._db.update(entity_type, entity_id, payload)
        if ok:
            self._dirty = True
        return ok

    def delete(self, entity_type: str, entity_id: int) -> bool:
        ok = self._db.delete(entity_type, entity_id)
        if ok:
            self._dirty = True
        return ok

    def flush(self) -> None:
        """Dipanggil saat graceful shutdown untuk memastikan data ter-commit."""
        self._db.commit()
        self._dirty = False
