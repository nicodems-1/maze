UV_RUN = uv run
PYTHON_VERSION = 3.13
MAIN = a_maze_ing.py
CONFIG = config.txt
MLX_WHL = mlx-2.2-py3-ubuntu-any.whl
WHL_COMPAT = mlx-2.2-py3-none-any.whl
VENV_DONE = .venv/.install_done
SRCS = srcs/visual.py \
       srcs/parsing.py \
       srcs/maze_solving.py \
       srcs/maze_generation.py \
       ./a_maze_ing.py

install: $(VENV_DONE)

$(WHL_COMPAT): $(MLX_WHL)
	@cp $(MLX_WHL) $(WHL_COMPAT)

$(VENV_DONE): pyproject.toml $(WHL_COMPAT)
	uv python install $(PYTHON_VERSION)
	uv sync
	uv pip install ./$(WHL_COMPAT)
	@touch $(VENV_DONE)

run: $(VENV_DONE) 
	$(UV_RUN) python $(MAIN) $(CONFIG)

debug:
	$(UV_RUN) python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .venv .mypy_cache __pycache__ $(WHL_COMPAT)

lint:
	$(UV_RUN) flake8 $(SRCS)
	$(UV_RUN) mypy $(SRCS) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV_RUN) flake8  $(SRCS)
	$(UV_RUN) mypy  $(SRCS) --strict

test_path:
	@pwd
	@ls -l a-maze-ing.py
	@echo "Variables SRCS: $(SRCS)"


.PHONY: install run debug clean lint lint-strict