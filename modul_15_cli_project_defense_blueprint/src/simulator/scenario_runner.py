"""
scenario_runner.py
--------------------
Menjalankan skenario demo urut dari A-Z (didefinisikan di
config/demo_scenarios.py), memastikan seluruh alur berjalan mulus
tanpa kegagalan saat sesi presentasi.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from config.demo_scenarios import DemoScenario, get_scenario  # noqa: E402
from src.simulator.auto_typer import type_prompt  # noqa: E402


class ScenarioExecutionError(RuntimeError):
    """Dilempar bila salah satu langkah skenario gagal dijalankan."""


def run_scenario(scenario: DemoScenario, speed: float = 0.03,
                  verbose: bool = True) -> list[str]:
    """
    Menjalankan seluruh langkah dalam sebuah DemoScenario secara berurutan.
    Mengembalikan log eksekusi (list string) untuk keperluan audit/testing.
    """
    log: list[str] = []
    log.append(f"=== Menjalankan skenario: {scenario.name} ===")
    log.append(scenario.description)

    for i, step in enumerate(scenario.steps, start=1):
        log.append(f"[Step {i}] {step.narration}")
        if verbose:
            print(f"\n> {step.narration}")
            type_prompt(step.command, delay=speed)
        time.sleep(0) if not verbose else time.sleep(min(step.delay_after, 0.5))
        log.append(f"  perintah: {step.command}")

    log.append("=== Skenario selesai tanpa error ===")
    return log


def run_by_name(name: str, speed: float = 0.03, verbose: bool = True) -> list[str]:
    scenario = get_scenario(name)
    return run_scenario(scenario, speed=speed, verbose=verbose)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "quick_tour"
    result_log = run_by_name(target)
    print("\n--- LOG EKSEKUSI ---")
    for line in result_log:
        print(line)
