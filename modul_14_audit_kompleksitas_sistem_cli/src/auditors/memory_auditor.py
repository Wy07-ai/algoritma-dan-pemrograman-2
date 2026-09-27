"""
src/auditors/memory_auditor.py
-------------------------------
Auditor konsumsi RAM berbasis `tracemalloc`, sekaligus pendeteksi
kebocoran memori (memory leak) dengan menjalankan fungsi target
berulang kali dan mengamati tren puncak memori antar-iterasi.
"""

import gc
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Callable

from config import settings


@dataclass
class MemoryAuditResult:
    function_name: str
    n: int
    peak_bytes_per_run: list = field(default_factory=list)

    @property
    def peak_mb_per_run(self) -> list:
        return [b / (1024 * 1024) for b in self.peak_bytes_per_run]

    @property
    def peak_mb(self) -> float:
        return max(self.peak_mb_per_run) if self.peak_mb_per_run else 0.0

    @property
    def leak_suspected(self) -> bool:
        """
        Heuristik sederhana: leak dicurigai jika puncak memori naik
        secara konsisten (monoton) melebihi toleransi di tiap iterasi.
        """
        runs = self.peak_mb_per_run
        if len(runs) < 2:
            return False
        tolerance = settings.MEMORY_LEAK_TOLERANCE_MB
        increasing_steps = sum(
            1 for a, b in zip(runs, runs[1:]) if (b - a) > tolerance
        )
        # Jika mayoritas langkah naik melewati toleransi -> curiga leak
        return increasing_steps >= max(1, len(runs) - 1)

    def to_dict(self) -> dict:
        return {
            "function": self.function_name,
            "n": self.n,
            "peak_mb": round(self.peak_mb, 4),
            "peak_mb_per_run": [round(v, 4) for v in self.peak_mb_per_run],
            "leak_suspected": self.leak_suspected,
        }


class MemoryAuditor:
    """Mengukur puncak penggunaan memori & mendeteksi indikasi leak."""

    def __init__(self, repeat: int = 5):
        self.repeat = repeat

    def measure(self, func: Callable, *args: Any, n: int = 0, **kwargs: Any) -> MemoryAuditResult:
        result = MemoryAuditResult(function_name=getattr(func, "__name__", str(func)), n=n)
        for _ in range(self.repeat):
            gc.collect()
            tracemalloc.start()
            func(*args, **kwargs)
            _current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            result.peak_bytes_per_run.append(peak)
        return result


if __name__ == "__main__":
    def dummy_build_list(n):
        return [i * i for i in range(n)]

    auditor = MemoryAuditor(repeat=4)
    res = auditor.measure(dummy_build_list, 200_000, n=200_000)
    print(res.to_dict())
