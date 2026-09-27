"""
src/ui/audit_dashboard.py
----------------------------
Menampilkan papan pemantau (dashboard) audit interaktif di terminal:
progres eksekusi tiap fungsi & skenario, lalu ringkasan akhir memakai
ScorePresenter.
"""

import sys
import time
from typing import Callable, Dict, List

from src.harness.scenario_runner import SCENARIOS, ScenarioRunner
from src.ui.score_presenter import ScorePresenter

BOLD = "\033[1m"
CYAN = "\033[96m"
RESET = "\033[0m"


class AuditDashboard:
    def __init__(self, runner: ScenarioRunner = None):
        self.runner = runner or ScenarioRunner()
        self.presenter = ScorePresenter()

    def _progress(self, message: str) -> None:
        sys.stdout.write(f"{CYAN}» {message}...{RESET}\n")
        sys.stdout.flush()

    def run(self, targets: Dict[str, Callable], scenarios: List[str] = None) -> dict:
        """
        targets: dict {nama_tampilan: fungsi_target}
        scenarios: daftar skenario yang ingin dijalankan (default: semua)
        """
        scenarios = scenarios or list(SCENARIOS.keys())
        all_results = {}

        print(f"{BOLD}=== AUDIT KOMPLEKSITAS SISTEM CLI ==={RESET}")
        print(f"Skala N diuji: {self.runner.n_scales} | Repetisi: {self.runner.repeat}\n")

        for name, func in targets.items():
            self._progress(f"Mengaudit fungsi '{name}'")
            per_scenario = {}
            for scenario in scenarios:
                start = time.time()
                report = self.runner.run(func, scenario)
                per_scenario[scenario] = report
                elapsed = time.time() - start
                self._progress(f"  Skenario '{scenario}' selesai ({elapsed:.2f}s nyata)")
            all_results[name] = per_scenario
            print()

        print(self.presenter.render_report(all_results))
        return all_results


if __name__ == "__main__":
    def sample_linear(data):
        target = -1
        for i, v in enumerate(data):
            if v == target:
                return i
        return -1

    dashboard = AuditDashboard(runner=ScenarioRunner(n_scales=[100, 1_000, 10_000]))
    dashboard.run({"linear_search": sample_linear})
