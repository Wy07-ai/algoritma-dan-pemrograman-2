"""
src/auditors/complexity_auditor.py
------------------------------------
Estimator kurva matematis yang menghitung kecocokan (fitting) Big-O
dari data empiris hasil audit (pasangan N -> waktu eksekusi).

Pendekatan: untuk tiap kandidat kelas kompleksitas g(N), cocokkan
model linear waktu = a*g(N) + b menggunakan least squares, lalu ukur
kualitas fit memakai *relative RMSE* (RMSE dibagi rata-rata waktu).
Metrik ini sengaja dipakai alih-alih R^2 klasik karena R^2 tidak
terdefinisi secara adil untuk kandidat O(1) (tidak ada variabel bebas),
sedangkan relative RMSE bisa dibandingkan apa adanya lintas semua
kandidat, termasuk O(1). Di antara kandidat yang error-nya nyaris
setara, dipilih kandidat paling sederhana (Occam's razor) agar model
kompleks tidak "menang" hanya karena kebetulan cocok dengan noise.
"""

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

CandidateFn = Callable[[float], float]

# Kandidat fungsi pertumbuhan g(N) untuk tiap kelas Big-O, terurut dari
# yang paling sederhana ke paling mahal. Urutan ini dipakai sebagai
# tie-breaker saat beberapa kandidat memiliki error yang hampir sama.
CANDIDATES: Dict[str, CandidateFn] = {
    "O(1)": lambda n: 1.0,
    "O(log N)": lambda n: math.log2(max(n, 2)),
    "O(N)": lambda n: n,
    "O(N log N)": lambda n: n * math.log2(max(n, 2)),
    "O(N^2)": lambda n: n ** 2,
    "O(2^N)": lambda n: 2 ** min(n, 60),  # dibatasi agar tidak overflow
}

# Selisih relative-error dianggap "setara" -> pilih model paling sederhana.
_ERROR_TIE_TOLERANCE = 0.05


@dataclass
class ComplexityFitResult:
    best_fit: str
    relative_error_by_candidate: Dict[str, float]

    def to_dict(self) -> dict:
        return {
            "best_fit": self.best_fit,
            "relative_error": {k: round(v, 5) for k, v in self.relative_error_by_candidate.items()},
        }


def _fit_relative_error(x: List[float], y: List[float]) -> float:
    """
    Mencocokkan y = a*x + b via least squares, mengembalikan RMSE
    relatif terhadap rata-rata y (coefficient-of-variation residual).
    Berlaku juga untuk x konstan (kandidat O(1)): saat itu prediksi
    terbaik adalah rata-rata y, sehingga metrik ini menjadi CV(y).
    """
    n = len(x)
    mean_y = sum(y) / n
    if mean_y == 0:
        mean_y = 1e-9  # hindari pembagian nol

    mean_x = sum(x) / n
    ss_xx = sum((xi - mean_x) ** 2 for xi in x)

    if ss_xx == 0:
        # x konstan -> prediksi terbaik = rata-rata y
        residuals = [yi - mean_y for yi in y]
    else:
        ss_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        slope = ss_xy / ss_xx
        intercept = mean_y - slope * mean_x
        residuals = [yi - (slope * xi + intercept) for xi, yi in zip(x, y)]

    rmse = math.sqrt(sum(r ** 2 for r in residuals) / n)
    return rmse / abs(mean_y)


class ComplexityAuditor:
    """Mengestimasi kelas Big-O paling cocok dari data (N, waktu)."""

    def fit(self, measurements: List[Tuple[int, float]]) -> ComplexityFitResult:
        """
        measurements: list of (n, time_ms), diurutkan atau tidak.
        Mengembalikan kandidat Big-O dengan relative error terendah,
        dengan tie-break ke kandidat paling sederhana.
        """
        measurements = sorted(measurements, key=lambda m: m[0])
        ns = [m[0] for m in measurements]
        times = [m[1] for m in measurements]

        errors: Dict[str, float] = {}
        for label, g in CANDIDATES.items():
            gx = [g(n) for n in ns]
            errors[label] = _fit_relative_error(gx, times)

        best_fit = self._select_simplest_within_tolerance(errors)
        return ComplexityFitResult(best_fit=best_fit, relative_error_by_candidate=errors)

    @staticmethod
    def _select_simplest_within_tolerance(errors: Dict[str, float]) -> str:
        best_error = min(errors.values())
        for label in CANDIDATES.keys():  # sudah terurut dari paling sederhana
            if errors[label] <= best_error + _ERROR_TIE_TOLERANCE:
                return label
        return min(errors, key=errors.get)


if __name__ == "__main__":
    # Contoh: data yang meniru pertumbuhan O(N)
    sample = [(100, 0.5), (1_000, 5.1), (10_000, 49.8), (100_000, 502.3)]
    auditor = ComplexityAuditor()
    fit = auditor.fit(sample)
    print(fit.to_dict())
