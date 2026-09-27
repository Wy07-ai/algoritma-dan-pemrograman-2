"""
src/storage/cache_store.py
-----------------------------
Penyimpan data sementara (caching) di RAM untuk mempercepat akses berulang,
mis. hasil query yang sering dipakai dalam satu sesi eksekusi. Menerapkan
kebijakan eviction sederhana: Least Recently Used (LRU) dengan batas
`max_items` agar memori tidak membengkak tanpa batas.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Optional


class CacheStore:
    """Cache in-memory berkapasitas tetap dengan strategi eviction LRU."""

    def __init__(self, max_items: int = 256) -> None:
        self._max_items = max_items
        self._store: "OrderedDict[str, Any]" = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        self._store.move_to_end(key)  # tandai baru saja diakses
        return self._store[key]

    def set(self, key: str, value: Any) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self._max_items:
            self._store.popitem(last=False)  # buang yang paling lama tak dipakai

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: str) -> bool:
        return key in self._store
