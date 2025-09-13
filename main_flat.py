# main_flat.py — flat-friendly runner for Zoran EU demo
import json, random, time, argparse, os, statistics, hashlib

def entropy(bits):
    if not bits:
        return 0.0
    values = {}
    for b in bits:
        values[b] = values.get(b, 0) + 1
    total = len(bits)
    import math
    H = 0.0
    for c in values.values():
        p = c / total
        H -= p * math.log(p + 1e-12, 2)
    Hmax = math.log(len(values) + 1e-12, 2)
    return H / (Hmax + 1e-12)

class ZDM:
    def __init__(self):
        self.short_term, self.long_term, self.resonant_cache, self.latent = [], [], [], []
    def ingest(self, event):
        self.short_term.append(event)
        if len(self.short_term) > 50:
            self.long_term.extend(self.short_term[:25])
            self.short_term = self.short_term[25:]
        sig = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()[:8]
        self.resonant_cache.append(sig)
        if len(self.resonant_cache) > 64:
            self.resonant_cache = self.resonant_cache[-64:]
    def state(self):
        return {"short":len(self.short_term),"long":len(self.long_term),"cache":len(self.resonant_cache),"latent":len(self.latent)}

class DeltaM113:
    def __init__(self, threshold=0.40):
        self.threshold, self.snapshots, self.rollbacks = threshold, [], 0
    def snapshot(self, zdm, history_bits):
        self.snapshots.append((list(zdm.short_term),list(zdm.long_term),list(zdm.resonant_cache),list(zdm.latent),list(history_bits)))
        if len(self.snapshots) > 8:
            self.snapshots = self.snapshots[-8:]
    def guard(self, zdm, history_bits):
        st = entropy(history_bits)
        if st < self.threshold and self.snapshots:
            (zdm.short_term, zdm.long_term, zdm.resonant_cache, zdm.latent, hb) = self.snapshots[-1]
            self.rollbacks += 1
            return True, st
        return False, st

def simulate(seed=42, steps=500, ablate=False):
    random.seed(seed)
    zdm, guard = ZDM(), DeltaM113(threshold=0.40)
    history_bits, t_latencies, coherences, rewards = [], [], [], []
    for t in range(steps):
        event = {"t": t, "domain": random.choice(["policy","tech","data"]), "signal": random.randint(0,1), "value": random.random()}
        t0 = time.time()
        zdm.ingest(event)
        parity = int(zdm.resonant_cache[-1], 16) % 2
        coherence = 1.0 if parity == event["signal"] else 0.0
        coherences.append(coherence)
        rewards.append(1.0 * coherence - 0.1 * (1 - coherence))
        history_bits.append(event["signal"])
        if len(history_bits) > 128:
            history_bits = history_bits[-128:]
        if not ablate:
            guard.snapshot(zdm, history_bits)
            rolled, st = guard.guard(zdm, history_bits)
        t1 = time.time()
        t_latencies.append((t1 - t0) * 1000.0)
    return {
        "seed": seed, "steps": steps,
        "coherence_avg": statistics.fmean(coherences),
        "latency_p95_ms": sorted(t_latencies)[int(0.95 * len(t_latencies))],
        "reward_avg": statistics.fmean(rewards),
        "rollbacks": 0 if ablate else guard.rollbacks,
        "zdm_state": zdm.state(),
        "ablate_mode": ablate,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--ablate", action="store_true")
    args = p.parse_args()
    m = simulate(seed=args.seed, steps=args.steps, ablate=args.ablate)
    # write at root (no directories)
    out = "metrics_ablation.json" if args.ablate else "metrics.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[seed={args.seed} steps={args.steps} ablate={args.ablate}] -> {out}\n")
    print(json.dumps(m, indent=2))

if __name__ == "__main__":
    main()
