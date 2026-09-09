.PHONY: all sim test numbers figures paper clean
# Experiments needing no licensed microdata
all: sim test numbers figures

sim:
	python3 experiments/exp01_shape_audit.py
	python3 experiments/exp05_information.py

# Experiments needing European Social Survey rounds 9-11; see docs/DATA.md
survey:
	python3 experiments/exp02_design_audit.py
	python3 experiments/exp03_regional.py
	python3 experiments/exp03b_verification.py
	python3 experiments/exp04_national.py
	python3 experiments/exp06_claims.py
	python3 experiments/exp07_widths.py
	python3 experiments/exp08_domains.py

test:
	python3 -m pytest tests/ -q

numbers:
	python3 paper/build_numbers.py

figures:
	python3 paper/figures.py

paper: numbers figures
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex
	cd paper && latexmk -pdf -interaction=nonstopmode titlepage.tex

clean:
	rm -f results/exp0*.csv results/exp0*.json
	cd paper && latexmk -C >/dev/null 2>&1 || true
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
