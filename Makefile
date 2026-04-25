POETRY_RUN = poetry run
PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.venv:
	uv tool install poetry
	poetry config virtualenvs.in-project true
	poetry install
	touch .venv

install: .venv

run:.venv
	$(POETRY_RUN) $(PYTHON) $(MAIN) $(CONFIG)

debug:.venv
	$(POETRY_RUN) $(PYTHON) -m pdb $(MAIN)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 srcs
	mypy srcs --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(POETRY_RUN) flake8 srcs a-maze-ing.py
	$(POETRY_RUN) mypy  srcs a-maze-ing.py --strict

.PHONY: install run debug clean lint lint-strict .venv
