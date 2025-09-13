.PHONY: reproduce_all risks audit fairness perf
reproduce_all: risks audit fairness perf

risks:
	python3 validate_yaml.py RISK_REGISTER.yaml
	node vex_check.js sbom.cdx.json vex.json

audit:
	python3 verify_c2pa.py decision_provenance.c2pa.json

fairness:
	python3 fairness_card.py data/decisions.csv --out FAIRNESS_CARD.json || true

perf:
	# Run with: k6 run perf_k6.js
	@echo "Perf placeholder. Use k6 to execute perf_k6.js"
