# AUDIT_NOTE

## Incohérences actuelles
1. Pas de tests automatisés (CI/CD absent)
2. Documentation dispersée par module
3. Versioning non structuré (RELEASE_LIST non semver)
4. Sécurité déclarée mais non démontrée

## Plan d’action
- Ajouter `tests/` + `.github/workflows/ci.yml`
- Écrire README par module (injecteur, parser, POC)
- Structurer RELEASE_LIST → CHANGELOG.md (SemVer)
- Démontrer Merkle logs & kill-switch
