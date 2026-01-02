# Makefile for building the docs

.PHONY: help clean html pdf

help:
	@echo "make html   - build HTML docs"
	@echo "make pdf    - build PDF docs (requires LaTeX)"
	@echo "make clean  - remove build artifacts"

clean:
	rm -rf _build

html:
	uv run sphinx-build -b html . _build/html

pdf:
	uv run sphinx-build -b latex . _build/latex
	cd _build/latex && make all-pdf
