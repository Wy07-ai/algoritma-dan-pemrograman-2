"""
test_demo_scenarios.py
------------------------
Menguji seluruh alur skenario demo otomatis agar tidak mengalami
kegagalan saat sesi presentasi/sidang berlangsung.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config.demo_scenarios import ALL_SCENARIOS, get_scenario  # noqa: E402
from src.simulator.scenario_runner import run_scenario  # noqa: E402


def test_all_scenarios_have_at_least_one_step():
    for name, scenario in ALL_SCENARIOS.items():
        assert len(scenario.steps) > 0, f"Skenario '{name}' tidak punya langkah"


def test_get_scenario_unknown_raises_keyerror():
    try:
        get_scenario("skenario_tidak_ada")
        assert False, "Seharusnya melempar KeyError"
    except KeyError:
        pass


def test_run_scenario_produces_complete_log():
    scenario = get_scenario("quick_tour")
    log = run_scenario(scenario, speed=0.0, verbose=False)
    assert log[0].startswith("=== Menjalankan skenario")
    assert log[-1] == "=== Skenario selesai tanpa error ==="
    # setiap step harus muncul di log
    assert sum(1 for line in log if line.startswith("[Step")) == len(scenario.steps)


def test_full_defense_scenario_runs_without_error():
    scenario = get_scenario("full_defense")
    log = run_scenario(scenario, speed=0.0, verbose=False)
    assert "=== Skenario selesai tanpa error ===" in log


if __name__ == "__main__":
    test_all_scenarios_have_at_least_one_step()
    test_get_scenario_unknown_raises_keyerror()
    test_run_scenario_produces_complete_log()
    test_full_defense_scenario_runs_without_error()
    print("Semua test demo scenarios LULUS.")
