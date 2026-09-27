"""
src/ui/score_presenter.py
---------------------------
Memvisualisasikan skor efisiensi sistem (Pass/Fail) per fungsi/skenario
dalam bentuk teks berwarna ANSI sederhana, tanpa dependensi eksternal.
"""

from typing import Any, Dict

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _color_status(status: str) -> str:
    if status == "PASS":
        return f"{GREEN}{BOLD}PASS{RESET}"
    return f"{RED}{BOLD}FAIL{RESET}"


class ScorePresenter:
    def render_function_summary(self, function_name: str, scenario_reports: Dict[str, Any]) -> str:
        lines = [f"{BOLD}=== {function_name} ==={RESET}"]
        pass_count = 0
        total = len(scenario_reports)

        for scenario_name, report in scenario_reports.items():
            sla = report.sla_result if hasattr(report, "sla_result") else report["sla_result"]
            fit = report.complexity_fit if hasattr(report, "complexity_fit") else report["complexity_fit"]
            status = sla["status"]
            if status == "PASS":
                pass_count += 1

            checks = sla["checks"]
            lines.append(
                f"  [{scenario_name:14s}] Big-O~{fit['best_fit']:10s} "
                f"time={checks['time']:4s} mem={checks['memory']:4s} "
                f"cplx={checks['complexity']:4s} -> {_color_status(status)}"
            )

        score_pct = (pass_count / total * 100) if total else 0.0
        color = GREEN if score_pct == 100 else (YELLOW if score_pct >= 50 else RED)
        lines.append(f"  Skor Efisiensi: {color}{score_pct:.0f}%{RESET} ({pass_count}/{total} skenario lulus)")
        return "\n".join(lines)

    def render_report(self, all_results: Dict[str, Dict[str, Any]]) -> str:
        blocks = [self.render_function_summary(name, scenarios) for name, scenarios in all_results.items()]
        return "\n\n".join(blocks)


if __name__ == "__main__":
    print("Modul score_presenter siap digunakan bersama scenario_runner.")
