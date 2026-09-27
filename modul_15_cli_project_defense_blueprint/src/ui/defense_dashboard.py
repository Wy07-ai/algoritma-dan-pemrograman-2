"""
defense_dashboard.py
----------------------
Dashboard ringkasan fitur & kompleksitas Big-O untuk ditunjukkan ke
dosen/penguji saat sesi sidang, merangkum hasil audit dari Modul 14.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class FeatureSummary:
    module_name: str
    description: str
    complexity: str
    status: str  # "READY" | "PARTIAL" | "PENDING"


DEFAULT_FEATURES: List[FeatureSummary] = [
    FeatureSummary("Modul 05 - Search", "Linear/Binary/Hash Search", "O(log N)", "READY"),
    FeatureSummary("Modul 06 - Sorting", "Bubble/Merge/Quick Sort", "O(N log N)", "READY"),
    FeatureSummary("Modul 09 - Resilience", "Circuit breaker & retry", "O(1) overhead", "READY"),
    FeatureSummary("Modul 10 - Hashing", "Custom hash table & LRU cache", "O(1) avg", "READY"),
    FeatureSummary("Modul 11 - Streaming", "Lazy pipeline & generators", "O(N) memory-safe", "READY"),
    FeatureSummary("Modul 14 - Audit", "SLA & complexity auditor", "N/A", "READY"),
]


def render_table(features: List[FeatureSummary] = DEFAULT_FEATURES) -> str:
    """Merender ringkasan fitur sebagai tabel teks sederhana untuk CLI."""
    headers = ["Modul", "Deskripsi", "Kompleksitas", "Status"]
    rows = [[f.module_name, f.description, f.complexity, f.status] for f in features]

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells: list[str]) -> str:
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    sep = "-+-".join("-" * w for w in widths)
    lines = [fmt_row(headers), sep] + [fmt_row(r) for r in rows]
    return "\n".join(lines)


def render_dashboard(features: List[FeatureSummary] = DEFAULT_FEATURES) -> str:
    ready = sum(1 for f in features if f.status == "READY")
    total = len(features)
    parts = [
        "=" * 60,
        " DEFENSE DASHBOARD — Ringkasan Fitur & Kompleksitas",
        "=" * 60,
        render_table(features),
        "-" * 60,
        f"Kesiapan sistem: {ready}/{total} modul READY "
        f"({ready / total * 100:.0f}%)",
        "=" * 60,
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    print(render_dashboard())
