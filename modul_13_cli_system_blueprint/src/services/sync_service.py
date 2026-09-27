"""
src/services/sync_service.py
--------------------------------
Layanan penyelaras data latar belakang (background synchronization).
Pada blueprint ini disederhanakan menjadi simulasi sinkronisasi lokal
(mis. menulis snapshot state ke berkas), sebagai titik ekstensi jika
kelak sistem terhubung ke server remote / cloud storage.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List


class SyncService:
    """Menyimpan snapshot data terbaru sebagai bentuk 'sinkronisasi lokal'."""

    def __init__(self, sync_dir: Path) -> None:
        self._sync_dir = sync_dir

    def sync(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        self._sync_dir.mkdir(parents=True, exist_ok=True)
        snapshot_path = self._sync_dir / "last_sync.json"

        result = {
            "synced_at": time.time(),
            "item_count": len(items),
            "status": "success",
        }

        snapshot_path.write_text(
            json.dumps({"meta": result, "items": items}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return result
