PYTHON       = python3
PIP          = pip3
MAIN_SCRIPT  = fly-in.py

EXCLUDE_DIRS = env,venv,.venv,.mypy_cache,__pycache__

MAP          ?= maps/subject_map.txt
SPEED        ?= 3

all: run

install:
	$(PIP) install pygame flake8 mypy

run:
	$(PYTHON) $(MAIN_SCRIPT) --speed $(SPEED) $(MAP)

run-debug:
	$(PYTHON) $(MAIN_SCRIPT) --debug --speed $(SPEED) $(MAP)

lint:
	flake8 . --exclude=$(EXCLUDE_DIRS)
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --explicit-package-bases \
		--exclude=$(EXCLUDE_DIRS)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: install run run-debug debug lint clean
