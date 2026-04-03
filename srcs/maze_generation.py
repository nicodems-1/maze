from random import randint


class Cell:
    """Cell class, each item contains it's x and y coordinates
    and if the cell has been visited"""
    def __init__(self, x: int, y: int) -> None:
        self.visited = False
        self.value = 0b1111
        self.x = x
        self.y = y


class MazeGenerator:
    def __init__(self, config:
    dict[str, int | tuple[int, int] | str | bool]) -> None:

        self.config = config
        self.width = self.config["WIDTH"]
        self.height = self.config["HEIGHT"]
        self.maze = [[Cell(x, y) for y in range(self.height)]
                     for x in range(self.width)]
        self.generate_maze()
        self.output = self.format_output()


    def generate_maze(self) -> None:
        current = Cell(randint(0, self.width -1),
                       randint(0, self.height -1))
        while self.unvisited_neighbours(current):
            current.visited = True
            unv = self.unvisited_neighbours(current)
            print(len(unv))
            chosen = unv[randint(0, len(unv) - 1)]
            self.break_wall(current, chosen)
            current = chosen

    def unvisited_neighbours(self, current: Cell) -> list[Cell]:
        unvisited_neighbours = []
        x = current.x
        y = current.y
        if x > 0 and not self.maze[x - 1][y].visited:
            unvisited_neighbours.append(self.maze[x - 1][y])
        if y > 0 and not self.maze[x][y - 1].visited:
            unvisited_neighbours.append(self.maze[x][y - 1])
        if x < self.width - 1 and not self.maze[x + 1][y].visited:
            unvisited_neighbours.append(self.maze[x + 1][y])
        if y < self.height - 1 and not self.maze[x][y + 1].visited:
            unvisited_neighbours.append(self.maze[x][y + 1])
        return unvisited_neighbours

    @staticmethod
    def break_wall(c1: Cell, c2: Cell) -> None:
        if c1.y > c2.y:
            c1.value &= 0b1110
            c2.value &= 0b1011
        if c1.x < c2.x:
            c1.value &= 0b1101
            c2.value &= 0b0111
        if c1.y < c2.y:
            c1.value &= 0b1011
            c2.value &= 0b1110
        if c1.x > c2.x:
            c1.value &= 0b0111
            c2.value &= 0b1101

    def format_output(self) -> str:
        output = ""

        i = 0
        while i < self.width:
            j = 0
            while j < self.height:
                output += str(hex(self.maze[i][j].value))[2:]
                j += 1
            output += "\n"
            i +=1
        return output
