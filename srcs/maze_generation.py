from random import randint


class Cell:
    """Cell class, each item contains it's x and y coordinates
    and if the cell has been visited"""
    def __init__(self, x: int, y: int) -> None:
        self.visited = False
        self.x = x
        self.y = y


class MazeGenerator:
    def __init__(self, config:dict[str, str]) -> None:
        self.config = config
        self.maze = list[list[Cell]]
        self.generate_maze()


    def generate_maze(self) -> None:
        current = Cell(randint(0, int(self.config["WIDTH"]) -1),
                       randint(0, int(self.config["HEIGHT"]) -1))
        current.visited = True
        while unvisited_neighbours(self.maze, current):


    def unvisited_neighbours(self, current: Cell) -> list:
        unvisited_neighbours = []
        x = current.x
        y = current.y
        if x > 0 and not (self.maze[x - 1][y]).visited:
            unvisited_neighbours.append(self.maze[x - 1][y])
        if y > 0 and not maze[x][y - 1].visited:
            unvisited_neighbours.append(maze[x][y - 1])
        if x < self.config["WIDTH"] - 1 and not maze
        return unvisited_neighbours