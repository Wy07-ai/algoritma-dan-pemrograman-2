"""
slide_deck_builder.py
----------------------
Mengonversi rangkuman metrik audit (dari Modul 14 - Audit Kompleksitas
Sistem CLI) menjadi konten slide presentasi teknis dalam format Markdown
(kompatibel dengan tool seperti Marp / Slidev / pandoc).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class AuditMetric:
    function_name: str
    avg_time_ms: float
    peak_memory_mb: float
    big_o_estimate: str
    sla_status: str  # "PASS" atau "FAIL"


@dataclass
class Slide:
    title: str
    bullets: List[str] = field(default_factory=list)


def build_title_slide(app_name: str, version: str, author: str) -> Slide:
    return Slide(
        title=f"{app_name} v{version}",
        bullets=[f"Dipresentasikan oleh: {author}", "Sesi: Project Defense"],
    )


def build_metrics_slide(metrics: List[AuditMetric]) -> Slide:
    bullets = []
    for m in metrics:
        bullets.append(
            f"{m.function_name}: {m.avg_time_ms:.2f} ms, "
            f"{m.peak_memory_mb:.2f} MB, {m.big_o_estimate} "
            f"→ {m.sla_status}"
        )
    return Slide(title="Ringkasan Hasil Audit Performa", bullets=bullets)


def build_conclusion_slide(pass_count: int, total_count: int) -> Slide:
    rate = (pass_count / total_count * 100) if total_count else 0
    return Slide(
        title="Kesimpulan",
        bullets=[
            f"{pass_count} dari {total_count} fungsi lulus kriteria SLA ({rate:.1f}%)",
            "Sistem siap untuk tahap rilis produksi",
        ],
    )


def render_markdown_deck(slides: List[Slide]) -> str:
    parts = []
    for slide in slides:
        parts.append(f"# {slide.title}\n")
        for b in slide.bullets:
            parts.append(f"- {b}")
        parts.append("\n---\n")
    return "\n".join(parts)


def build_deck(app_name: str, version: str, author: str,
               metrics: List[AuditMetric]) -> str:
    pass_count = sum(1 for m in metrics if m.sla_status == "PASS")
    slides = [
        build_title_slide(app_name, version, author),
        build_metrics_slide(metrics),
        build_conclusion_slide(pass_count, len(metrics)),
    ]
    return render_markdown_deck(slides)


if __name__ == "__main__":
    sample_metrics = [
        AuditMetric("binary_search", 0.02, 0.5, "O(log N)", "PASS"),
        AuditMetric("bubble_sort", 12.4, 1.2, "O(N^2)", "FAIL"),
        AuditMetric("hash_lookup", 0.005, 0.3, "O(1)", "PASS"),
    ]
    deck = build_deck("CLI Project Defense Suite", "1.0.0",
                       "Tim Pengembang Algo2", sample_metrics)
    print(deck)
