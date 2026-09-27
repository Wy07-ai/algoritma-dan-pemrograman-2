"""
src/ui_engine/view_router.py
-------------------------------
Menghubungkan output dari service layer ke tampilan CLI. Bertugas
memformat data mentah (dict/list) menjadi teks yang enak dibaca di
terminal, tanpa mencampur logika bisnis ke dalam kode presentasi.
"""

from __future__ import annotations

from typing import Any, Dict, List


class ViewRouter:
    """Formatter tampilan untuk berbagai jenis hasil operasi."""

    def render_item(self, item: Dict[str, Any]) -> str:
        if not item:
            return "(item tidak ditemukan)"
        return (
            f"#{item.get('id')} | {item.get('name')}\n"
            f"    {item.get('description') or '-'}\n"
            f"    dibuat: {item.get('created_at')}"
        )

    def render_item_list(self, items: List[Dict[str, Any]]) -> str:
        if not items:
            return "(belum ada data)"

        lines = [f"Total item: {len(items)}", "-" * 40]
        for item in items:
            desc = item.get("description") or "-"
            lines.append(f"[{item.get('id'):>3}] {item.get('name'):<20} {desc}")
        return "\n".join(lines)

    def render_message(self, message: str, ok: bool = True) -> str:
        prefix = "[OK]" if ok else "[GAGAL]"
        return f"{prefix} {message}"
