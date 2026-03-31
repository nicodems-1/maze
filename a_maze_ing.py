#!/usr/bin/env python3
from srcs.parsing import Parser
from srcs.maze_generation import MazeGenerator
import sys


def main() -> None:
    """Main function of the program"""
    if len(sys.argv) != 2:
        print("usage: 'python3 a_maze_ing.py <config_file>' or 'make run "
              "<config_file>'\n[ERROR] Missing config file target",
              file=sys.stderr)
    try:
        config = Parser().config
        maze = MazeGenerator(config).maze
    except Exception as e:
        print(e, file=sys.stderr)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}", file=sys.stderr)
