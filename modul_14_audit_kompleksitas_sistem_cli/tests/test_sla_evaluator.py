"""
tests/test_sla_evaluator.py
------------------------------
Memverifikasi validitas logika penilaian kriteria SLA
(config/SLA_benchmarks.py) agar hasil evaluasi bersifat objektif
dan konsisten.
"""

import unittest

from config.SLA_benchmarks import SLARule, evaluate, get_sla


class TestSLARegistry(unittest.TestCase):
    def test_known_function_returns_specific_rule(self):
        rule = get_sla("binary_search")
        self.assertEqual(rule.max_growth_class, "O(log N)")

    def test_unknown_function_returns_default_rule(self):
        rule = get_sla("fungsi_tidak_terdaftar")
        self.assertIsInstance(rule, SLARule)


class TestSLAEvaluation(unittest.TestCase):
    def test_pass_when_all_within_bounds(self):
        result = evaluate(
            function_name="binary_search",
            time_ms=10,
            memory_mb=5,
            detected_bigo="O(log N)",
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checks"]["time"], "PASS")
        self.assertEqual(result["checks"]["memory"], "PASS")
        self.assertEqual(result["checks"]["complexity"], "PASS")

    def test_fail_when_time_exceeds_sla(self):
        result = evaluate(
            function_name="binary_search",
            time_ms=999,
            memory_mb=5,
            detected_bigo="O(log N)",
        )
        self.assertEqual(result["checks"]["time"], "FAIL")
        self.assertEqual(result["status"], "FAIL")

    def test_fail_when_complexity_worse_than_target(self):
        # binary_search seharusnya O(log N); jika empiris malah O(N^2) -> FAIL
        result = evaluate(
            function_name="binary_search",
            time_ms=1,
            memory_mb=1,
            detected_bigo="O(N^2)",
        )
        self.assertEqual(result["checks"]["complexity"], "FAIL")
        self.assertEqual(result["status"], "FAIL")

    def test_pass_when_complexity_better_than_target(self):
        # Jika target O(N) tapi hasil empiris O(log N) (lebih baik) -> tetap PASS
        result = evaluate(
            function_name="linear_search",
            time_ms=1,
            memory_mb=1,
            detected_bigo="O(log N)",
        )
        self.assertEqual(result["checks"]["complexity"], "PASS")


if __name__ == "__main__":
    unittest.main()
