# TM-ZDM-STRIDE-2025

## Portée
- Composants: ZDM.HardCore (persistant, conformité), ZDM.ResonantCache (phase/cache), ΔM11.3 (rollback), EthicChain (politiques), Merkle/C2PA (traçabilité)

## STRIDE
- **S**poofing: usurpation d’identités d’agents → Mitigation: mTLS mutualisé, PQC (Kyber/Dilithium), attestation exécutable
- **T**ampering: altération du cache résonant → Mitigation: hash chain + Merkle log, C2PA sur snapshots, quorum write
- **R**epudiation: déni d’écriture → Mitigation: journaux immuables (append-only), signatures, horodatage TSP
- **I**nformation disclosure: fuite mémoire latente → Mitigation: redaction by policy, labels de confidentialité, enclaves
- **D**enial of Service: saturation rollback ΔM11.3 → Mitigation: backoff exponentiel, budgets de compute, circuit-breaker
- **E**levation of privilege: escalade via policies → Mitigation: policy engine RO + 4-yeux, tests de conformité

## Arbre d’attaque (extrait)
But: Corrompre ZDM.ResonantCache → (A) corrompre flux d’entrée → (A1) injection hors schéma → (mit: schema validation, rate limit) ; (A2) clé invalide → (mit: KMS, rotation, mTLS) → (B) forcer rollback storm → (mit: ΔM11.3 throttle, quorum).
