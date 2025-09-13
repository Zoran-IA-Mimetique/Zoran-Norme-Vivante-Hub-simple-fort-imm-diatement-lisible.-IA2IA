.PHONY: run ablation reproduce_all clean
run:
	python3 main_flat.py --seed 42 --steps 500
ablation:
	python3 main_flat.py --seed 42 --steps 500 --ablate
reproduce_all: run ablation
clean:
	rm -f metrics.json metrics_ablation.json logs.txt
