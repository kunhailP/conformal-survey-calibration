.PHONY: all exp01 test numbers paper clean
all: exp01 test numbers
numbers:
	python3 paper/build_numbers.py
paper: numbers
	cd paper && latexmk -pdf main.tex
exp01:
	python3 experiments/exp01_shape_audit.py
test:
	python3 -m pytest tests/ -q
clean:
	rm -f results/exp01_*.csv results/exp01_*.json
	find . -name __pycache__ -type d -exec rm -rf {} +
