.PHONY: all sim test numbers figures paper clean
# Experiments needing no licensed microdata
all: sim test numbers figures

sim:
	python3 experiments/exp01_shape_audit.py
	python3 experiments/exp05_information.py
	python3 experiments/exp09_estimated_variance.py
	python3 experiments/exp10_certification.py
	python3 experiments/exp11_heteroscedastic.py
	python3 experiments/exp12_closing_scalar.py
	python3 experiments/exp13_weights_and_containment.py
	python3 experiments/exp14_chain.py
	python3 experiments/exp15_diagnosis.py
	python3 experiments/exp16_band_comparison.py
	python3 experiments/exp17_complex_sample.py
	python3 experiments/exp18_regional_share.py
	python3 experiments/exp19_headroom.py
	python3 experiments/exp20_ratio_pivot.py
	python3 experiments/exp21_estimated_structure.py
	python3 experiments/exp22_completion.py
	python3 experiments/exp23_certified.py
	python3 experiments/exp24_survey_structure.py
	python3 experiments/exp25_high_share.py
	python3 experiments/exp26_same_target.py
	python3 experiments/exp29_scale_law.py
	python3 experiments/exp30_necessary_condition.py

# Experiments needing European Social Survey rounds 9-11; see docs/DATA.md
survey:
	python3 experiments/exp02_design_audit.py
	python3 experiments/exp03_regional.py
	python3 experiments/exp03b_verification.py
	python3 experiments/exp04_national.py
	python3 experiments/exp06_claims.py
	python3 experiments/exp07_widths.py
	python3 experiments/exp08_domains.py
	python3 experiments/exp27_ess_scalar.py
	python3 experiments/exp28_centring.py

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
