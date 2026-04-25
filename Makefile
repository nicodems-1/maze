UV_RUN = uv run
PYTHON_VERSION = 3.12
MAIN = a_maze_ing.py
CONFIG = config.txt
MLX_WHL = mlx-2.2-py3-ubuntu-any.whl
WHL_COMPAT = mlx-2.2-py3-none-any.whl

.PHONY: all install run debug clean lint lint-strict 

all: install

install: $(WHL_COMPAT)
	uv python install $(PYTHON_VERSION)
	uv sync
	uv pip install ./$(WHL_COMPAT)

$(WHL_COMPAT):
	@cp $(MLX_WHL) $(WHL_COMPAT)

run: install 
	$(UV_RUN) python $(MAIN) $(CONFIG)

debug:.venv
	$(UV_RUN) python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .venv .mypy_cache __pycache__ $(WHL_COMPAT)

lint:
	$(UV_RUN) flake8 srcs a-maze-ing.py
	$(UV_RUN) mypy srcs --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV_RUN) flake8  srcs a-maze-ing.py
	$(UV_RUN) mypy  srcs a-maze-ing.py --strict

