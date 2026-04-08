#!/usr/bin/env python3
from srcs.parsing import Parser
from srcs.maze_generation import generate_maze
from srcs.visual import Visual
import sys


def main() -> None:
    """Main function of the program"""
    sys.setrecursionlimit(10000)

    if len(sys.argv) != 2:
        print("usage: 'python3 a_maze_ing.py <config_file>' or 'make run "
              "<config_file>'\n[ERROR] Missing config file target",
              file=sys.stderr)
        return

    # try:
    config = Parser().config
    maze_obj = generate_maze(config)
    mlx_obj = Visual(maze_obj, config)
    mlx_obj.run_win()
    # except Exception as e:
    #     print(f"{e}", file=sys.stderr)


if __name__ == '__main__':
    main()
