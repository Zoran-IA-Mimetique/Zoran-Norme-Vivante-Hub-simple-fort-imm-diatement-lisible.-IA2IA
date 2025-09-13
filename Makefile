PY=python3

simulate:
	$(PY) algos/fairdispatch.py --seed 42 --steps 500 --segments 6 --services 4 --budget 1000000 --theta 0.03 --out tests/data/sim_result.json

test:
	$(PY) -m pytest -q || echo "pytest not installed; tests skipped"

docs:
	which pandoc >/dev/null 2>&1 && pandoc docs/IMRaD.md -o docs/IMRaD.pdf || echo "Install pandoc to build PDFs"

sbom:
	which cyclonedx-py >/dev/null 2>&1 && cyclonedx-py -o sbom/cyclonedx.json || echo "Install cyclonedx-py to generate SBOM"
