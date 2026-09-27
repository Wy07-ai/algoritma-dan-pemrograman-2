"""
config/SLA_benchmarks.py
------------------------
Standar batas kriteria Lulus/Gagal (Pass/Fail) untuk audit performa.

Setiap fungsi yang diaudit bisa didaftarkan di SLA_REGISTRY dengan
batas waktu (ms) dan batas memori (MB) sendiri. Jika suatu fungsi
tidak terdaftar, sistem memakai DEFAULT_SLA dari config/settings.py.
"""

from dataclasses import dataclass
from config import settings


@dataclass
class SLARule:
    max_time_ms: float
    max_memory_mb: float
    max_growth_class: str  # salah satu dari BIGO_ORDER di bawah


# Urutan kompleksitas dari yang paling cepat ke paling lambat.
# Dipakai untuk membandingkan "apakah hasil audit lebih buruk dari target".
BIGO_ORDER = ["O(1)", "O(log N)", "O(N)", "O(N log N)", "O(N^2)", "O(2^N)"]


def _rank(bigo: str) -> int:
    return BIGO_ORDER.index(bigo) if bigo in BIGO_ORDER else len(BIGO_ORDER)


# Registry contoh: nama fungsi -> aturan SLA spesifik.
SLA_REGISTRY = {
    "linear_search": SLARule(max_time_ms=200, max_memory_mb=64, max_growth_class="O(N)"),
    "binary_search": SLARule(max_time_ms=50, max_memory_mb=32, max_growth_class="O(log N)"),
    "bubble_sort": SLARule(max_time_ms=2000, max_memory_mb=64, max_growth_class="O(N^2)"),
    "quick_sort": SLARule(max_time_ms=300, max_memory_mb=64, max_growth_class="O(N log N)"),
}

DEFAULT_SLA = SLARule(
    max_time_ms=settings.MAX_EXECUTION_TIME_MS,
    max_memory_mb=settings.MAX_MEMORY_MB,
    max_growth_class="O(N log N)",
)


def get_sla(function_name: str) -> SLARule:
    """Ambil aturan SLA untuk fungsi tertentu, fallback ke default."""
    return SLA_REGISTRY.get(function_name, DEFAULT_SLA)


def evaluate(function_name: str, time_ms: float, memory_mb: float, detected_bigo: str) -> dict:
    """
    Mengevaluasi hasil audit empiris terhadap SLA yang berlaku.
    Mengembalikan dict berisi status per-kriteria dan status akhir.
    """
    rule = get_sla(function_name)

    time_pass = time_ms <= rule.max_time_ms
    memory_pass = memory_mb <= rule.max_memory_mb
    complexity_pass = _rank(detected_bigo) <= _rank(rule.max_growth_class)

    overall_pass = time_pass and memory_pass and complexity_pass

    return {
        "function": function_name,
        "sla": rule,
        "measured": {"time_ms": time_ms, "memory_mb": memory_mb, "bigo": detected_bigo},
        "checks": {
            "time": "PASS" if time_pass else "FAIL",
            "memory": "PASS" if memory_pass else "FAIL",
            "complexity": "PASS" if complexity_pass else "FAIL",
        },
        "status": "PASS" if overall_pass else "FAIL",
    }
