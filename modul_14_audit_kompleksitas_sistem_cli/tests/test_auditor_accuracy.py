"""
tests/test_auditor_accuracy.py
--------------------------------
Menguji presisi dan keakuratan alat ukur profiler waktu dan memori,
serta akurasi estimator kompleksitas (complexity_auditor).
"""

import time
import unittest

from src.auditors.complexity_auditor import ComplexityAuditor
from src.auditors.memory_auditor import MemoryAuditor
from src.auditors.time_auditor import TimeAuditor


def sleep_a_bit(_data=None):
    time.sleep(0.02)  # 20 ms


def allocate_list(n):
    return [0] * n


class TestTimeAuditor(unittest.TestCase):
    def test_measures_positive_duration(self):
        auditor = TimeAuditor(repeat=3)
        result = auditor.measure(sleep_a_bit, n=0)
        self.assertGreater(result.mean_ms, 0)

    def test_reflects_actual_sleep_duration(self):
        auditor = TimeAuditor(repeat=3)
        result = auditor.measure(sleep_a_bit, n=0)
        # Toleransi longgar untuk jitter OS scheduler
        self.assertGreaterEqual(result.mean_ms, 15)
        self.assertLessEqual(result.mean_ms, 200)

    def test_sample_count_matches_repeat(self):
        auditor = TimeAuditor(repeat=7)
        result = auditor.measure(sleep_a_bit, n=0)
        self.assertEqual(len(result.samples_ms), 7)


class TestMemoryAuditor(unittest.TestCase):
    def test_larger_allocation_uses_more_memory(self):
        auditor = MemoryAuditor(repeat=2)
        small = auditor.measure(allocate_list, 1_000, n=1_000)
        large = auditor.measure(allocate_list, 1_000_000, n=1_000_000)
        self.assertLess(small.peak_mb, large.peak_mb)

    def test_stable_allocation_not_flagged_as_leak(self):
        auditor = MemoryAuditor(repeat=4)
        result = auditor.measure(allocate_list, 10_000, n=10_000)
        self.assertFalse(result.leak_suspected)


class TestComplexityAuditor(unittest.TestCase):
    def test_detects_linear_growth(self):
        # waktu (ms) yang meniru kurva O(N) hampir sempurna
        data = [(100, 1.0), (1_000, 10.0), (10_000, 100.0), (100_000, 1000.0)]
        fit = ComplexityAuditor().fit(data)
        self.assertEqual(fit.best_fit, "O(N)")

    def test_detects_constant_time(self):
        data = [(100, 5.0), (1_000, 5.1), (10_000, 4.9), (100_000, 5.05)]
        fit = ComplexityAuditor().fit(data)
        self.assertEqual(fit.best_fit, "O(1)")

    def test_detects_quadratic_growth(self):
        data = [(10, 1.0), (20, 4.0), (40, 16.0), (80, 64.0)]
        fit = ComplexityAuditor().fit(data)
        self.assertEqual(fit.best_fit, "O(N^2)")


if __name__ == "__main__":
    unittest.main()
