"""
src/services/data_service.py
-------------------------------
Layanan utama pengolah logika bisnis dan manipulasi data entitas.
Berkomunikasi HANYA lewat Repository (src/storage/repository.py),
tidak pernah mengakses LocalDB secara langsung, agar business logic
tetap independen dari mekanisme storage fisik.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.storage.cache_store import CacheStore
from src.storage.repository import Repository

ENTITY_TYPE = "item"


class DataService:
    """Operasi bisnis atas entitas 'item' dengan dukungan cache read-through."""

    def __init__(self, repository: Repository, cache: CacheStore) -> None:
        self._repo = repository
        self._cache = cache

    def create_item(self, name: str, description: str = "") -> Dict[str, Any]:
        if not name or not name.strip():
            raise ValueError("Nama item tidak boleh kosong.")

        payload = {"name": name.strip(), "description": description.strip()}
        new_id = self._repo.add(ENTITY_TYPE, payload)
        item = self._repo.get(ENTITY_TYPE, new_id)
        self._cache.set(self._cache_key(new_id), item)
        return item

    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        cached = self._cache.get(self._cache_key(item_id))
        if cached is not None:
            return cached

        item = self._repo.get(ENTITY_TYPE, item_id)
        if item is not None:
            self._cache.set(self._cache_key(item_id), item)
        return item

    def list_items(self) -> List[Dict[str, Any]]:
        return self._repo.list_all(ENTITY_TYPE)

    def update_item(self, item_id: int, **fields: Any) -> bool:
        current = self._repo.get(ENTITY_TYPE, item_id)
        if current is None:
            return False

        current.update({k: v for k, v in fields.items() if v is not None})
        current.pop("id", None)
        current.pop("created_at", None)

        ok = self._repo.update(ENTITY_TYPE, item_id, current)
        if ok:
            self._cache.invalidate(self._cache_key(item_id))
        return ok

    def delete_item(self, item_id: int) -> bool:
        ok = self._repo.delete(ENTITY_TYPE, item_id)
        if ok:
            self._cache.invalidate(self._cache_key(item_id))
        return ok

    @staticmethod
    def _cache_key(item_id: int) -> str:
        return f"{ENTITY_TYPE}:{item_id}"
