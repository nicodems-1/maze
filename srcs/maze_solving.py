from srcs.maze_generation import MazeGenerator, Cell


def solve_maze(config: dict, maze_obj: MazeGenerator) -> str:
    maze = maze_obj.maze
    n = maze_obj.height
    m = maze_obj.width
    x_entry = config["ENTRY"][1]
    y_entry = config["ENTRY"][0]
    x_exit = config["EXIT"][1]
    y_exit = config["EXIT"][0]
    entry = (x_entry, y_entry)
    directions = {(-1, 0): "N",
                  (0, 1): "E",
                  (1, 0): "S",
                  (0, -1): "W"}

    queue = [entry]
    history = {entry: ((x_entry, y_entry), "ENTRY POINT")}
    while queue:
        i, j = queue.pop(0)
        if (i, j) == (x_exit, y_exit):
            return _reconstruct_path(history, i, j, x_entry, y_entry)
        for di, dj in directions:
            ni = i + di
            nj = j + dj
            if (0 <= ni < n and 0 <= nj < m
                    and (ni, nj) not in history
                    and _is_not_blocked(maze[i][j], maze[ni][nj])):
                history[(ni, nj)] = ((i, j), directions[(di, dj)])
                queue.append((ni, nj))
    return "Did not find exit :/"


def _reconstruct_path(history, i, j, x_entry, y_entry) -> str:
    path = []
    node = (i, j)
    while node != (x_entry, y_entry):
        parent, direction = history[node]
        path.append(direction)
        node = parent
    return "".join(reversed(path))


def _is_not_blocked(c1: Cell, c2: Cell) -> bool:
    if c1.x > c2.x:
        return not bool(c1.value & 0b0001)
    if c1.y < c2.y:
        return not bool(c1.value & 0b0010)
    if c1.x < c2.x:
        return not bool(c1.value & 0b0100)
    if c1.y > c2.y:
        return not bool(c1.value & 0b1000)
    return False
