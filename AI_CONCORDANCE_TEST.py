#!/usr/bin/env python3
import json, sys, statistics, hashlib
TOL = 0.03
SRC = sys.argv[1] if len(sys.argv) > 1 else 'codex_propositions_200.json'

def sha512i(t):
    return hashlib.sha512(t.encode('utf-8')).hexdigest()

with open(SRC, 'r', encoding='utf-8') as f:
    laws = json.load(f)

diffs = []
for law in laws:
    S = (law['beta'] * law['delta_Ce']) / law['lambda']
    deltaS = S - law['S_calc']
    diffs.append(deltaS)
    status = 'OK' if abs(deltaS) <= TOL else 'DRIFT'
    print(f"{law['id']} ΔS={deltaS:+.3f} → {status}")

mean = statistics.mean(diffs)
std = statistics.pstdev(diffs)
concordance = 1 - abs(mean)
with open('ΔBias-Audit.json', 'w', encoding='utf-8') as out:
    json.dump({'mean_ΔS': mean, 'std_ΔS': std, 'P_AI_global': concordance}, out, indent=2)
print(f"ΔS moy={mean:+.4f} σ={std:.4f} → Pᴬᴵ≈{concordance:.3%}")
