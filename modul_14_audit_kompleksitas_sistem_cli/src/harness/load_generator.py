"""
src/harness/load_generator.py
-------------------------------
Pembuat dan penyuntik beban data masukan sintetis secara otomatis
dalam rentang skala N=100 hingga N=1.000.000 (atau skala kustom).
"""

import random
from typing import List

from config.settings import DEFAULT_N_SCALES


class LoadGenerator:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def random_ints(self, n: int, low: int = 0, high: int = 1_000_000) -> List[int]:
        return [self.rng.randint(low, high) for _ in range(n)]

    def sorted_ints(self, n: int) -> List[int]:
        return list(range(n))

    def reversed_ints(self, n: int) -> List[int]:
        return list(range(n, 0, -1))

    def nearly_sorted_ints(self, n: int, swap_fraction: float = 0.02) -> List[int]:
        data = list(range(n))
        swaps = max(1, int(n * swap_fraction))
        for _ in range(swaps):
            i, j = self.rng.randrange(n), self.rng.randrange(n)
            data[i], data[j] = data[j], data[i]
        return data

    def generate_scales(self, scales: List[int] = None) -> List[int]:
        return scales if scales is not None else list(DEFAULT_N_SCALES)


if __name__ == "__main__":
    gen = LoadGenerator()
    for n in gen.generate_scales([10, 100, 1000]):
        sample = gen.random_ints(n)
        print(f"N={n} -> contoh 5 elemen pertama: {sample[:5]}")
