# IMRaD — Zoran SOINS

## Introduction
Défi: administrer la santé avec **équité mesurable** et **preuve** (traçabilité C2PA, SBOM), tout en respectant AI Act/RGPD/MDR.

## Methods
Architecture ZDM (HardCore + Resonant cache), ΔM11.3, PolyResonator (UCB1), EthicChain/Aegis. Interop FHIR/openEHR/DICOM.

## Results (simulation)
Voir `algos/fairdispatch.py` : amélioration attendue de l'indice d'équité F (1 - Gini pondéré) et réduction p95 des temps de traitement.
Seeds: 13/42/101; Welch t-test; ablations −ΔM11.3/−ZDM/−C2PA.

## Discussion
Complexité gérée par **composabilité** (bounded contexts), ADRs, et Policy-as-code. Performance ZDM par caches hiérarchiques (W-TinyLFU) + φ-signatures.

## Conclusion
Zoran SOINS fournit une ossature **polymorphe** et **auditée**, prête à cloner vers d'autres domaines.

## Limitations
Données synthétiques; MDR hors-scope de ce skeleton; dépendances d'interop locales.

## Ethics & Governance
EthicChain (règles versionnées) + Aegis (veto, human-in-command, kill-switch multi-sig).
