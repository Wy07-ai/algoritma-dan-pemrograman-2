"""
src/auditors/time_auditor.py
-----------------------------
Profiler tingkat mikrodetik yang mengukur latensi dan waktu respons
sebuah fungsi CLI. Menjalankan fungsi target beberapa kali (repeat)
untuk mendapatkan statistik yang stabil (min, max, mean, median).
"""

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class TimeAuditResult:
    function_name: str
    n: int
    samples_ms: list = field(default_factory=list)

    @property
    def min_ms(self) -> float:
        return min(self.samples_ms)

    @property
    def max_ms(self) -> float:
        return max(self.samples_ms)

    @property
    def mean_ms(self) -> float:
        return statistics.mean(self.samples_ms)

    @property
    def median_ms(self) -> float:
        return statistics.median(self.samples_ms)

    @property
    def stdev_ms(self) -> float:
        return statistics.stdev(self.samples_ms) if len(self.samples_ms) > 1 else 0.0

    def to_dict(self) -> dict:
        return {
            "function": self.function_name,
            "n": self.n,
            "min_ms": round(self.min_ms, 4),
            "max_ms": round(self.max_ms, 4),
            "mean_ms": round(self.mean_ms, 4),
            "median_ms": round(self.median_ms, 4),
            "stdev_ms": round(self.stdev_ms, 4),
        }


class TimeAuditor:
    """Mengukur latensi eksekusi fungsi target secara presisi."""

    def __init__(self, repeat: int = 5):
        self.repeat = repeat

    def measure(self, func: Callable, *args: Any, n: int = 0, **kwargs: Any) -> TimeAuditResult:
        result = TimeAuditResult(function_name=getattr(func, "__name__", str(func)), n=n)
        for _ in range(self.repeat):
            start = time.perf_counter()
            func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            result.samples_ms.append(elapsed_ms)
        return result


if __name__ == "__main__":
    # Contoh pemakaian mandiri
    def dummy_linear_search(data, target):
        for i, v in enumerate(data):
            if v == target:
                return i
        return -1

    auditor = TimeAuditor(repeat=5)
    sample_data = list(range(100_000))
    res = auditor.measure(dummy_linear_search, sample_data, -1, n=len(sample_data))
    print(res.to_dict())
