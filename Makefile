PYTHON ?= python3

.PHONY: help validate test build check serve sync clean

help:
	@echo "Aalimiyah Directory developer commands"
	@echo "  make check     Run tests, validate data, and build the site"
	@echo "  make serve     Build and preview at http://127.0.0.1:8000"
	@echo "  make sync      Import the configured Google Sheet CSV"
	@echo "  make validate  Validate data/courses.csv"
	@echo "  make test      Run the Python test suite"
	@echo "  make build     Assemble the deployable _site directory"
	@echo "  make clean     Remove generated local files"

validate:
	$(PYTHON) scripts/validate_data.py

test:
	$(PYTHON) -m unittest discover -s tests -v

build: validate
	$(PYTHON) scripts/build_site.py

check:
	$(PYTHON) scripts/check_project.py

serve: build
	$(PYTHON) -m http.server 8000 --directory _site

sync:
	$(PYTHON) scripts/sync_sheet.py
	$(PYTHON) scripts/validate_data.py

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(path, ignore_errors=True) for path in (Path('_site'), Path('scripts/__pycache__'), Path('tests/__pycache__'))]"
