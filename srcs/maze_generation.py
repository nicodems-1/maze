from random import randint


class Cell:
    """Cell class, each item contains it's x and y coordinates
    and if the cell has been visited"""
    def __init__(self, x: int, y: int) -> None:
        self.visited = False
        self.hex = 0xF
        self.x = x
        self.y = y


class MazeGenerator:
    def __init__(self, config:
    dict[str, int | tuple[int, int] | str | bool]) -> None:

        self.config = config
        self.maze = [[Cell(x, y) for y in range(self.config["HEIGHT"])]
                     for x in range(self.config["WIDTH"])]
        self.generate_maze()


    def generate_maze(self) -> None:
        current = Cell(randint(0, self.config["WIDTH"] -1),
                       randint(0, self.config["HEIGHT"] -1))
        current.visited = True
        while self.unvisited_neighbours(current):
            unv = self.unvisited_neighbours(current)
            chosen = unv[randint(0, len(unv))]
            #TODO: self.break_wall(current, chosen)
            current = chosen

    def unvisited_neighbours(self, current: Cell) -> list[Cell]:
        unvisited_neighbours = []
        x = current.x
        y = current.y
        if x > 0 and not self.maze[x - 1][y].visited:
            unvisited_neighbours.append(self.maze[x - 1][y])
        if y > 0 and not self.maze[x][y - 1].visited:
            unvisited_neighbours.append(self.maze[x][y - 1])
        if x < self.config["WIDTH"] - 1 and not self.maze[x + 1][y].visited:
            unvisited_neighbours.append(self.maze[x + 1][y])
        if y < self.config["HEIGHT"] - 1 and not self.maze[x][y + 1].visited:
            unvisited_neighbours.append(self.maze[x][y + 1])
        return unvisited_neighbours