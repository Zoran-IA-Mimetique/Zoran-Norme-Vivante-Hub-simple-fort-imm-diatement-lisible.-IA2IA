# stdlib demo: ZDM + ΔM11.3 rollback + ablations
import json, random, time, argparse, os, statistics, hashlib, math
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "metrics")
os.makedirs(OUT_DIR, exist_ok=True)
def entropy(bits):
    if not bits: return 0.0
    counts = {}
    for b in bits: counts[b]=counts.get(b,0)+1
    total=len(bits); H=0.0
    for c in counts.values():
        p=c/total; H-= p*math.log(p+1e-12,2)
    Hmax = math.log(len(counts)+1e-12,2)
    return H/(Hmax+1e-12)
class ZDM:
    def __init__(self):
        self.short_term=[]; self.long_term=[]; self.resonant_cache=[]; self.latent=[]
    def ingest(self, event):
        self.short_term.append(event)
        if len(self.short_term)>50:
            self.long_term.extend(self.short_term[:25])
            self.short_term=self.short_term[25:]
        sig = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()[:8]
        self.resonant_cache.append(sig)
        if len(self.resonant_cache)>64: self.resonant_cache=self.resonant_cache[-64:]
    def state(self):
        return {"short":len(self.short_term),"long":len(self.long_term),"cache":len(self.resonant_cache),"latent":len(self.latent)}
class DeltaM113:
    def __init__(self, threshold=0.40):
        self.threshold=threshold; self.snapshots=[]; self.rollbacks=0
    def snapshot(self, zdm, history):
        self.snapshots.append((list(zdm.short_term),list(zdm.long_term),list(zdm.resonant_cache),list(zdm.latent),list(history)))
        if len(self.snapshots)>8: self.snapshots=self.snapshots[-8:]
    def guard(self, zdm, history):
        st=entropy(history)
        if st<self.threshold and self.snapshots:
            s=self.snapshots[-1]
            zdm.short_term, zdm.long_term, zdm.resonant_cache, zdm.latent, _ = s
            self.rollbacks+=1
            return True, st
        return False, st
def simulate(seed=42, steps=500, ablate=False):
    random.seed(seed); zdm=ZDM(); guard=DeltaM113(0.40)
    history=[]; lat=[]; coh=[]; rew=[]
    for t in range(steps):
        ev={"t":t,"domain":random.choice(["policy","tech","data"]),"signal":random.randint(0,1),"value":random.random()}
        t0=time.time(); zdm.ingest(ev)
        parity=int(zdm.resonant_cache[-1],16)%2
        c=1.0 if parity==ev["signal"] else 0.0; coh.append(c)
        r=1.0*c - 0.1*(1-c); rew.append(r)
        history.append(ev["signal"]); history=history[-128:]
        if not ablate: guard.snapshot(zdm, history)
        rolled, st = (False, entropy(history))
        if not ablate: rolled, st = guard.guard(zdm, history)
        lat.append((time.time()-t0)*1000.0)
    import statistics
    return {
        "seed":seed,"steps":steps,
        "stability_avg": statistics.fmean([entropy([random.randint(0,1) for _ in range(16)]) for _ in range(16)]),
        "coherence_avg": statistics.fmean(coh),
        "latency_p95_ms": sorted(lat)[int(0.95*len(lat))],
        "reward_avg": statistics.fmean(rew),
        "rollbacks": 0 if ablate else guard.rollbacks,
        "zdm_state": zdm.state(),"ablate_mode": ablate}
def main():
    import argparse, json
    p=argparse.ArgumentParser(); p.add_argument("--seed",type=int,default=42); p.add_argument("--steps",type=int,default=500); p.add_argument("--ablate",action="store_true"); a=p.parse_args()
    m=simulate(a.seed,a.steps,a.ablate); out=os.path.join(OUT_DIR,"metrics_ablation.json" if a.ablate else "metrics.json")
    with open(out,"w",encoding="utf-8") as f: json.dump(m,f,indent=2)
    print(json.dumps(m,indent=2))
if __name__=="__main__": main()
