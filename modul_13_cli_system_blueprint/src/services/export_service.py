"""
src/services/export_service.py
----------------------------------
Layanan pendukung untuk mengekspor laporan data menjadi berkas eksternal
(JSON / CSV) di luar sistem penyimpanan utama.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


class ExportService:
    """Mengonversi daftar entitas menjadi berkas JSON atau CSV."""

    def export_to_json(self, items: List[Dict[str, Any]], destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
        return destination

    def export_to_csv(self, items: List[Dict[str, Any]], destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)

        if not items:
            destination.write_text("", encoding="utf-8")
            return destination

        fieldnames = sorted({key for item in items for key in item.keys()})
        with destination.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
        return destination
