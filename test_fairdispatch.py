import json, os
from algos.fairdispatch import simulate

def test_simulation_runs(tmp_path):
    res = simulate(seed=13, T=200, n_segments=4, n_services=3, B_total=100000, theta=0.05)
    assert 0.0 <= res["final_F"] <= 1.0
    assert len(res["segments"]) == 4
