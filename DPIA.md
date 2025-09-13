# DPIA — Data Protection Impact Assessment (template)

## 1. Description du traitement
- Finalités: soins, remboursements, équité, recherche (data trust).
- Données: FHIR R4 (patient, consent, claim...), pseudonymisation φ-signature (ZDM).

## 2. Base légale
- Soins: intérêt vital/mission d'intérêt public. Recherche: consentement explicite/granulaire.

## 3. Analyse des risques
- Fuites, biais, discrimination indirecte, attaques de reconstruction.

## 4. Mesures
- Minimisation, TTL, cache résonant, ΔM11.3, audit C2PA/Sigstore, tests d'équité. 

## 5. Consultation DPO/Aegis
- DPO signe la DPIA; Aegis valide les garde-fous.
