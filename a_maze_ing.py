#!/usr/bin/env python3
from srcs.parsing import Parser
from srcs.maze_generation import MazeGenerator
from srcs.visual import Visual
from srcs.maze_solving import solve_maze
import sys
import random


def generate_and_solve_maze(config) -> MazeGenerator:
    if config.get("SEED") is not None:
        random.seed(config.get("SEED"))
    maze_obj = MazeGenerator(config)
    solve_maze(config, maze_obj)

    try:
        with open(config["OUTPUT_FILE"], "w") as output:
            output.write(str(maze_obj.output))
            output.write("\n")
            output.write(str(config["ENTRY"])[1:-1] + "\n")
            output.write(str(config["EXIT"])[1:-1] + "\n")
            output.write(maze_obj.directions)

    except OSError as e:
        raise OSError(f"[OSError]: {e}")

    return maze_obj


def main() -> None:
    """Main function of the program"""
    sys.setrecursionlimit(10000)

    if len(sys.argv) != 2:
        print(
            "usage: 'python3 a_maze_ing.py <config_file>' or 'make run "
            "<config_file>'\n[ERROR] Missing config file target",
            file=sys.stderr,
        )
        return

    try:
        config = Parser().config
        maze_obj = generate_and_solve_maze(config)
        mlx_obj = Visual(maze_obj, config)
        mlx_obj.run_win()

    except Exception as e:
        print(f"{e}", file=sys.stderr)


if __name__ == "__main__":
    main()
