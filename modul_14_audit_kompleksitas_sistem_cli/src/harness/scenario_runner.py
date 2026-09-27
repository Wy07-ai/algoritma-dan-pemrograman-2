"""
src/harness/scenario_runner.py
--------------------------------
Penguji skenario eksekusi komprehensif untuk menguji kondisi
Best Case, Average Case, dan Worst Case pada tiap fungsi target,
lintas beberapa skala N. Menggabungkan hasil time/memory auditor,
mengestimasi Big-O empiris, lalu mengevaluasi terhadap SLA.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List

from config import settings
from config.SLA_benchmarks import evaluate as evaluate_sla
from src.auditors.complexity_auditor import ComplexityAuditor
from src.auditors.memory_auditor import MemoryAuditor
from src.auditors.time_auditor import TimeAuditor
from src.harness.load_generator import LoadGenerator

# Skenario data: nama -> generator method name di LoadGenerator
SCENARIOS = {
    "best_case": "sorted_ints",
    "average_case": "random_ints",
    "worst_case": "reversed_ints",
}


@dataclass
class ScenarioAuditReport:
    function_name: str
    scenario: str
    per_n_results: List[dict] = field(default_factory=list)
    complexity_fit: dict = field(default_factory=dict)
    sla_result: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "function": self.function_name,
            "scenario": self.scenario,
            "per_n_results": self.per_n_results,
            "complexity_fit": self.complexity_fit,
            "sla_result": self.sla_result,
        }


class ScenarioRunner:
    def __init__(self, n_scales: List[int] = None, repeat: int = None):
        self.n_scales = n_scales or settings.DEFAULT_N_SCALES
        self.repeat = repeat or settings.REPEAT_COUNT
        self.load_gen = LoadGenerator()
        self.time_auditor = TimeAuditor(repeat=self.repeat)
        self.memory_auditor = MemoryAuditor(repeat=self.repeat)
        self.complexity_auditor = ComplexityAuditor()

    def run(self, func: Callable, scenario: str = "average_case") -> ScenarioAuditReport:
        if scenario not in SCENARIOS:
            raise ValueError(f"Skenario tidak dikenal: {scenario}")

        func_name = getattr(func, "__name__", str(func))
        gen_method = getattr(self.load_gen, SCENARIOS[scenario])

        per_n_results = []
        measurements_for_fit = []

        for n in self.n_scales:
            data = gen_method(n)
            time_res = self.time_auditor.measure(func, data, n=n)
            memory_res = self.memory_auditor.measure(func, data, n=n)

            per_n_results.append({
                "n": n,
                "time": time_res.to_dict(),
                "memory": memory_res.to_dict(),
            })
            measurements_for_fit.append((n, time_res.mean_ms))

        fit = self.complexity_auditor.fit(measurements_for_fit)

        # Ambil pengukuran skala terbesar sebagai representasi "worst realistic"
        largest = per_n_results[-1]
        sla_result = evaluate_sla(
            function_name=func_name,
            time_ms=largest["time"]["mean_ms"],
            memory_mb=largest["memory"]["peak_mb"],
            detected_bigo=fit.best_fit,
        )

        return ScenarioAuditReport(
            function_name=func_name,
            scenario=scenario,
            per_n_results=per_n_results,
            complexity_fit=fit.to_dict(),
            sla_result=sla_result,
        )

    def run_all_scenarios(self, func: Callable) -> Dict[str, ScenarioAuditReport]:
        return {scenario: self.run(func, scenario) for scenario in SCENARIOS}


if __name__ == "__main__":
    def linear_search(data):
        target = -1  # sengaja tidak ada, memaksa worst-case penuh
        for i, v in enumerate(data):
            if v == target:
                return i
        return -1

    runner = ScenarioRunner(n_scales=[100, 1_000, 10_000])
    report = runner.run(linear_search, "average_case")
    print(report.to_dict())
