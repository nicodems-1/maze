from random import randint
from typing import TypedDict


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


class Cell:
    """Cell class, each item contains it's x and y coordinates
    and if the cell has been visited"""

    def __init__(self, x: int, y: int) -> None:
        self.visited = False
        self.value = 0b1111
        self.x = x
        self.y = y


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.width: int = config["WIDTH"]
        self.height: int = config["HEIGHT"]

        self.maze = [
            [Cell(x, y) for y in range(self.width)] for x in range(self.height)
        ]

        self.directions: str = ""
        self.path: list[tuple[int, int]] = []
        self.output: str = ""

        self.generate_maze()
        if not self.config["PERFECT"]:
            self.create_alt_path()
        self.solve_maze()
        self.format_output()
        self.write_output()

    def generate_maze(self) -> None:
        if self.width > 8 and self.height > 6:
            self.put_42()
        self.dfs_algorithm(self.maze[0][0])

    def solve_maze(self) -> None:
        from .maze_solving import maze_solver
        maze_solver(self)


    def dfs_algorithm(self, current: Cell) -> None:
        current.visited = True
        while self.unvisited_neighbours(current):
            unv = self.unvisited_neighbours(current)
            chosen = unv[randint(0, len(unv) - 1)]
            self.break_wall(current, chosen)
            self.dfs_algorithm(chosen)

    def format_output(self) -> None:
        i = 0
        while i < self.height:
            j = 0
            while j < self.width:
                self.output += str(hex(self.maze[i][j].value))[2:]
                j += 1
            self.output += "\n"
            i += 1

    def write_output(self) -> None:
        try:
            with open(self.config["OUTPUT_FILE"], "w") as output:
                output.write(str(self.output))
                output.write("\n")
                output.write(str(self.config["ENTRY"])[1:-1] + "\n")
                output.write(str(self.config["EXIT"])[1:-1] + "\n")
                output.write(self.directions)

        except OSError as e:
            raise OSError(f"[OSError]: {e}")

    def create_alt_path(self) -> None:
        direction = randint(0, 1)
        x = 0
        y = 0

        if direction == 0:
            while (
                self.maze[x][y].value & 0b0010 == 0
                or self.maze[x][y].value == 0b1111
                or self.maze[x][y + 1].value == 0b1111
            ):
                y += 1
                if y == self.width - 1:
                    x += 1
                    y = 0
            self.break_wall(self.maze[x][y], self.maze[x][y + 1])

        if direction == 1:
            while (
                self.maze[x][y].value & 0b0100 == 0
                or self.maze[x][y].value == 0b1111
                or self.maze[x + 1][y].value == 0b1111
            ):
                x += 1
                if x == self.height - 1:
                    x = 0
                    y += 1
            self.break_wall(self.maze[x][y], self.maze[x + 1][y])

    def unvisited_neighbours(self, current: Cell) -> list[Cell]:
        unvisited_neighbours = []
        x = current.x
        y = current.y
        if x > 0 and self.maze[x - 1][y].visited is False:
            unvisited_neighbours.append(self.maze[x - 1][y])
        if y > 0 and self.maze[x][y - 1].visited is False:
            unvisited_neighbours.append(self.maze[x][y - 1])
        if x < self.height - 1 and self.maze[x + 1][y].visited is False:
            unvisited_neighbours.append(self.maze[x + 1][y])
        if y < self.width - 1 and self.maze[x][y + 1].visited is False:
            unvisited_neighbours.append(self.maze[x][y + 1])
        return unvisited_neighbours

    @staticmethod
    def break_wall(c1: Cell, c2: Cell) -> None:
        if c1.x > c2.x:
            c1.value &= 0b1110
            c2.value &= 0b1011
        if c1.y < c2.y:
            c1.value &= 0b1101
            c2.value &= 0b0111
        if c1.x < c2.x:
            c1.value &= 0b1011
            c2.value &= 0b1110
        if c1.y > c2.y:
            c1.value &= 0b0111
            c2.value &= 0b1101

    def put_42(self) -> None:
        logo = []
        x = int(self.height / 2) - 2
        y = int(self.width / 2) - 3
        for i in range(0, 2):
            self.maze[x][y].visited = True
            x += 1
        for i in range(0, 2):
            self.maze[x][y].visited = True
            y += 1
        for i in range(0, 3):
            self.maze[x][y].visited = True
            x += 1
        x -= 1
        y += 4
        for i in range(0, 2):
            self.maze[x][y].visited = True
            logo.append((x, y))
            y -= 1
        for i in range(0, 2):
            self.maze[x][y].visited = True
            logo.append((x, y))
            x -= 1
        for i in range(0, 2):
            self.maze[x][y].visited = True
            logo.append((x, y))
            y += 1
        for i in range(0, 2):
            self.maze[x][y].visited = True
            logo.append((x, y))
            x -= 1
        for i in range(0, 3):
            self.maze[x][y].visited = True
            logo.append((x, y))
            y -= 1
        if self.config["EXIT"] in logo:
            raise ValueError("[PARSING ERROR] Exit cannot be in the 42 logo")
        if self.config["ENTRY"] in logo:
            raise ValueError("[PARSING ERROR] Entry cannot be in the 42 logo")
