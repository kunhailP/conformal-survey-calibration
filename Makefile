.PHONY: all exp01 test clean
all: exp01 test
exp01:
	python3 experiments/exp01_shape_audit.py
test:
	python3 -m pytest tests/ -q
clean:
	rm -f results/exp01_*.csv results/exp01_*.json
	find . -name __pycache__ -type d -exec rm -rf {} +
