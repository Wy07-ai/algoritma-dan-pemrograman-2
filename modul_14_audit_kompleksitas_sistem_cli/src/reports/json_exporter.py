"""
src/reports/json_exporter.py
------------------------------
Ekspor raw data hasil audit (per-fungsi, per-skenario) ke berkas JSON
mentah, agar bisa dianalisis lebih lanjut oleh alat lain.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

from config import settings


class JSONExporter:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or settings.REPORTS_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, audit_data: Dict[str, Any], filename: str = None) -> str:
        if filename is None:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            filename = f"audit_report_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)
        payload = {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data": audit_data,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
        return filepath


if __name__ == "__main__":
    exporter = JSONExporter(output_dir="/tmp/audit_reports_demo")
    path = exporter.export({"example_function": {"status": "PASS"}})
    print(f"Laporan JSON tersimpan di: {path}")
