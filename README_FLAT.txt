# Zoran EU — Mode FLAT (zéro dossier)
Ce paquet à **plat** place tous les fichiers à la racine. Utilise `main_flat.py` et ce Makefile pour exécuter la démo **sans sous-dossiers**.

## Exécution
make reproduce_all
# ou
python3 main_flat.py --seed 42 --steps 500
python3 main_flat.py --seed 42 --steps 500 --ablate

## Sorties générées (à la racine) :
- metrics.json
- metrics_ablation.json
- logs.txt
