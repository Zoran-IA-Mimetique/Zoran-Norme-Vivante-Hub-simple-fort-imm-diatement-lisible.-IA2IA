def codex_memory_sum(laws, proofs, ethics):
    return sum(l * p * e for l, p, e in zip(laws, proofs, ethics))

if __name__ == "__main__":
    laws = [1.1, 1.0, 0.9, 1.2, 1.05, 1.0, 1.15, 0.95, 1.1, 1.08]
    proofs = [0.98, 1.0, 1.02, 0.97, 1.0, 1.03, 0.99, 1.01, 1.0, 1.02]
    ethics = [1.0, 1.02, 0.99, 1.03, 1.01, 1.0, 1.02, 1.01, 0.98, 1.0]
    delta_m = codex_memory_sum(laws, proofs, ethics)
    print("ΔM_{Codex} =", round(delta_m, 4))
    if 9.5 <= delta_m <= 10.5:
        print("Cohérence du Codex validée : système unifié.")
    else:
        print("Anomalie détectée : recalibrage EthicChain requis.")
