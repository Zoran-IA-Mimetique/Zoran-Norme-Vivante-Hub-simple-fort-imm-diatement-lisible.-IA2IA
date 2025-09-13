import argparse, json, random
from algos.ucb1 import UCB1
from algos.fairness_metrics import fairness_index
from algos.drift_guard import guard_fairness

def normalize(x, lo, hi, invert=False):
    if hi == lo:
        return 0.5
    v = (x - lo) / (hi - lo)
    v = max(0.0, min(1.0, v))
    return 1.0 - v if invert else v

def composite_outcome(seg_metrics, ranges, weights):
    # seg_metrics keys: qaly_gain, wait_days, claim_days, coverage, readmit_rate
    # ranges dict: min/max per metric for normalization
    # weights dict: per metric
    qaly = normalize(seg_metrics['qaly_gain'], *ranges['qaly_gain'])
    wait = normalize(seg_metrics['wait_days'], *ranges['wait_days'], invert=True)
    claim = normalize(seg_metrics['claim_days'], *ranges['claim_days'], invert=True)
    cov = normalize(seg_metrics['coverage'], *ranges['coverage'])
    readm = normalize(seg_metrics['readmit_rate'], *ranges['readmit_rate'], invert=True)
    return (weights['qaly_gain']*qaly +
            weights['wait_days']*wait +
            weights['claim_days']*claim +
            weights['coverage']*cov +
            weights['readmit_rate']*readm)

def simulate(seed=42, T=2000, n_segments=6, n_services=4, B_total=1000000, theta=0.03):
    rng = random.Random(seed)
    # Initial synthetic segments with vulnerability weights and populations
    segments = []
    for i in range(n_segments):
        seg = {
            "name": f"seg_{i}",
            "population": rng.randint(20000, 120000),
            "vulnerability": rng.choice([1.0, 1.25, 1.5]),  # extra weight
            # baseline metrics (to be improved by services)
            "qaly_gain": rng.uniform(0.2, 0.6),
            "wait_days": rng.uniform(10, 45),
            "claim_days": rng.uniform(3, 14),
            "coverage": rng.uniform(0.55, 0.85),
            "readmit_rate": rng.uniform(0.08, 0.22)
        }
        segments.append(seg)

    # metric ranges for normalization (could be learned from data)
    ranges = {
        "qaly_gain": (0.0, 1.0),
        "wait_days": (0.0, 60.0),
        "claim_days": (0.0, 21.0),
        "coverage": (0.0, 1.0),
        "readmit_rate": (0.0, 0.35)
    }
    metric_w = {"qaly_gain":0.35, "wait_days":0.20, "claim_days":0.15, "coverage":0.20, "readmit_rate":0.10}

    # Initialize allocations evenly
    allocation = [B_total / n_segments for _ in range(n_segments)]
    # Service arms with different improvement profiles (stochastic)
    service_profiles = []
    for k in range(n_services):
        prof = {
            "qaly_gain": rng.uniform(0.001, 0.006),
            "wait_days": -rng.uniform(0.05, 0.25),
            "claim_days": -rng.uniform(0.02, 0.15),
            "coverage": rng.uniform(0.001, 0.004),
            "readmit_rate": -rng.uniform(0.0005, 0.003)
        }
        service_profiles.append(prof)

    ucb = UCB1(n_services)
    # compute initial fairness
    values = []
    weights = []
    for seg in segments:
        v = composite_outcome(seg, ranges, metric_w)
        values.append(v)
        weights.append(seg["population"] * seg["vulnerability"])
    F_prev = fairness_index(values, weights)

    history = [{"t":0, "F":F_prev, "alloc": allocation.copy()}]

    for t in range(1, T+1):
        # choose service arm
        k = ucb.select()
        # choose a target segment (vulnerable or with worse outcomes)
        target = min(range(n_segments), key=lambda i: composite_outcome(segments[i], ranges, metric_w))
        # spend marginal budget
        dB = B_total / (T*0.8)  # shrinking marginal
        allocation[target] += dB

        # apply stochastic improvement to target segment
        prof = service_profiles[k]
        noise = lambda s: rng.gauss(0, s)
        segments[target]['qaly_gain'] = max(0.0, min(1.0, segments[target]['qaly_gain'] + prof['qaly_gain'] + noise(0.001)))
        segments[target]['wait_days'] = max(0.0, segments[target]['wait_days'] + prof['wait_days'] + noise(0.1))
        segments[target]['claim_days'] = max(0.0, segments[target]['claim_days'] + prof['claim_days'] + noise(0.05))
        segments[target]['coverage'] = max(0.0, min(1.0, segments[target]['coverage'] + prof['coverage'] + noise(0.001)))
        segments[target]['readmit_rate'] = max(0.0, segments[target]['readmit_rate'] + prof['readmit_rate'] + noise(0.0005))

        # compute reward for chosen service (aligned with composite outcome improvement & fairness)
        values = [composite_outcome(s, ranges, metric_w) for s in segments]
        weights = [s["population"]*s["vulnerability"] for s in segments]
        F = fairness_index(values, weights)
        reward = (sum(values)/len(values)) + (F - F_prev)  # encourage mean improvement + fairness drift

        # guard: rollback if fairness drops beyond theta
        if guard_fairness(F_prev, F, theta):
            # revert allocation and partial metric change
            allocation[target] -= dB
            # small corrective noise (reverse step)
            segments[target]['qaly_gain'] = max(0.0, segments[target]['qaly_gain'] - prof['qaly_gain']*0.5)
            segments[target]['wait_days'] = max(0.0, segments[target]['wait_days'] - prof['wait_days']*0.5)
            segments[target]['claim_days'] = max(0.0, segments[target]['claim_days'] - prof['claim_days']*0.5)
            segments[target]['coverage'] = max(0.0, min(1.0, segments[target]['coverage'] - prof['coverage']*0.5))
            segments[target]['readmit_rate'] = max(0.0, segments[target]['readmit_rate'] - prof['readmit_rate']*0.5)
            F = F_prev  # restore
            reward = 0.0

        ucb.update(k, reward)
        F_prev = F
        if t % max(1, T//10) == 0:
            history.append({"t":t, "F":F, "alloc": allocation.copy()})

    result = {
        "final_F": F_prev,
        "segments": segments,
        "allocation": allocation,
        "history": history
    }
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--segments", type=int, default=6)
    p.add_argument("--services", type=int, default=4)
    p.add_argument("--budget", type=float, default=1_000_000)
    p.add_argument("--theta", type=float, default=0.03)
    p.add_argument("--out", type=str, default="tests/data/sim_result.json")
    args = p.parse_args()
    res = simulate(seed=args.seed, T=args.steps, n_segments=args.segments, n_services=args.services, B_total=args.budget, theta=args.theta)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps({"final_F":res["final_F"], "history_points":len(res["history"])}))

if __name__ == "__main__":
    main()
