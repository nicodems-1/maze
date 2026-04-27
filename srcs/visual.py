from mlx import Mlx # type: ignore
import random
from srcs.maze_generation import MazeGenerator # type: ignore
from typing import Callable, Dict, Tuple, Union, cast

ConfigDict = Dict[str, Union[int, Tuple[int, int], str, bool]]


class Visual:
    mlx_instance: Mlx
    mlx_ptr: int
    win_ptr: int
    img_ptr: int
    img_data: bytearray
    bpp: int
    size_line: int
    endian: int
    cell: int
    center_x: int
    center_y: int
    horizontal_cells: int
    vertical_cells: int

    def __init__(self, maze_obj: MazeGenerator, config: ConfigDict) -> None:
        self.maze_obj = maze_obj
        self.config = config
        self.draw: bool = False
        self.mlx_instance = Mlx()
        self.mlx_ptr: int = self.mlx_instance.mlx_init()

        self.width = 0
        self.height = 0
        self.win_ptr = 0
        self.cell = 0
        self.center_x = 0
        self.center_y = 0
        self.horizontal_cells = 0
        self.vertical_cells = 0

        self.create_window()
        self.img_ptr = self.mlx_instance.mlx_new_image(
            self.mlx_ptr, self.width, self.height
        )
        self.img_data, self.bpp, self.size_line, self.endian = (
            self.mlx_instance.mlx_get_data_addr(self.img_ptr)
        )
        self.check = 0
        self.vertical_color = (255, 255, 255)
        self.horizontal_color = (255, 255, 255)
        self.log_color = (255, 0, 0)
        height_val = cast(int, self.config["HEIGHT"])
        width_val = cast(int, self.config["WIDTH"])
        self.padding = max(height_val, width_val)

        self.key_map = {
            99: self.change_color,
            113: self.close_window,
            114: self.regenerate,
            115: self.path_draw,
        }

    def handle_input(self, keycode: int, params: Callable):
        func = self.key_map.get(keycode)
        if func:
            func()

    def close_window(self):
        self.mlx_instance.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx_instance.mlx_loop_exit(self.mlx_ptr)

    def change_color(self):
        self.vertical_color, self.horizontal_color = self.random_colors()
        _, self.log_color = self.random_colors()
        self.display_maze()
        if self.draw is True:
            self.draw = False
            self.path_draw()

    def regenerate(self):
        from a_maze_ing import generate_and_solve_maze

        self.draw = False
        self.maze_obj = generate_and_solve_maze(self.config)
        self.display_maze()

    def create_window(self):
        _, self.width, self.height = self.mlx_instance.mlx_get_screen_size(
            self.mlx_ptr
        )
        self.win_ptr = self.mlx_instance.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "a-maze-ing"
        )

    def generate_cells(self, hexa: int, x_offset: int, y_offset: int):
        # creating line
        if hexa & 1 == 1:
            for i in range(self.cell):
                self.put_pixel(
                    self.center_x + x_offset + i,
                    self.center_y + y_offset,
                    *self.horizontal_color,
                )
        # creating column
        if hexa & 8 == 8:
            for i in range(self.cell):
                self.put_pixel(
                    self.center_x + x_offset,
                    self.center_y + i + y_offset,
                    *self.vertical_color,
                )

    def display_maze(self):
        self.create_maze(str(self.maze_obj.output))
        x, y = self.real_pos(self.config["ENTRY"])
        j, q = self.real_pos(self.config["EXIT"])
        self.fill_path(x, y, (255, 0, 0))
        self.fill_path(j, q, (0, 255, 0))
        self.mlx_instance.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        logo_placement = 50
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr, self.win_ptr, logo_placement, 50, int("0000FF", 16), "ENTRY"
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr, self.win_ptr, logo_placement, 70, int("00FF00", 16), "EXIT"
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            logo_placement,
            90,
            int("FFE100", 16),
            "C : Change color",
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            logo_placement,
            110,
            int("FFE100", 16),
            "Q : Close window",
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            logo_placement,
            130,
            int("FFE100", 16),
            "S : Show/hide path",
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            logo_placement,
            150,
            int("FFE100", 16),
            "R : Regenerate Maze",
        )
        self.mlx_instance.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

    def put_pixel(self, x: int, y: int, r: int, g: int, b: int):
        index = (y * self.size_line) + (x * (self.bpp // 8))

        self.img_data[index] = b
        self.img_data[index + 1] = g
        self.img_data[index + 2] = r
        self.img_data[index + 3] = 255

    def fill_square(self, offset_x: int, offset_y: int):
        for u in range(self.cell):
            for i in range(self.cell):
                self.put_pixel(
                    self.center_x + offset_x + i,
                    self.center_y + offset_y + u,
                    *self.log_color,
                )
            u += 1

    def fill_path(self, offset_x: int, offset_y: int, color: tuple):
        for u in range(self.cell - int((self.cell / 2))):
            for i in range(self.cell - int((self.cell / 2))):
                self.put_pixel(
                    self.center_x + offset_x + i + int((self.cell / 2) / 2),
                    self.center_y + offset_y + u + int((self.cell / 2) / 2),
                    *color,
                )
            u += 1

    def create_maze(self, parsed: str):
        self.img_data[:] = b"\x00" * len(self.img_data)
        lines = parsed.splitlines()

        # mesuring the size of the maze
        self.horizontal_cells = len(lines[0])
        self.vertical_cells = len(lines)

        # centering maze with padding
        self.cell = self.width // (self.vertical_cells + self.padding)
        self.center_x = int(
            (self.width - (self.cell * self.horizontal_cells)) / 2
        )
        self.center_y = int(
            (self.height - (self.cell * self.vertical_cells)) / 2
        )
        # creating the maze, cell by cell
        y_offset = -self.cell
        x_offset = 0
        for line in lines:
            x_offset = 0
            y_offset += self.cell
            for letter in line:
                nbr = int(letter, 16)
                self.generate_cells(nbr, x_offset, y_offset)
                if nbr == 15:
                    self.fill_square(x_offset, y_offset)
                x_offset += self.cell
        self.close_maze()

    def path_draw(self):
        if self.draw is False:
            the_path = self.maze_obj.path
            for pos in the_path:
                y, x = self.real_pos(pos)
                self.fill_path(x, y, (255, 78, 0))
            self.mlx_instance.mlx_put_image_to_window(
                self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
            )
            self.draw = True
        elif self.draw is True:
            the_path = self.maze_obj.path
            for pos in the_path:
                y, x = self.real_pos(pos)
                self.fill_path(x, y, (0, 0, 0))
            self.mlx_instance.mlx_put_image_to_window(
                self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
            )
            self.draw = False

    def real_pos(self, pos: tuple) -> tuple:
        x, y = pos
        real_x = self.cell * x
        real_y = self.cell * y
        return (real_x, real_y)

    def close_maze(self):
        for i in range(self.cell * self.horizontal_cells):
            self.put_pixel(
                self.center_x + i,
                self.center_y + self.vertical_cells * self.cell,
                *self.horizontal_color,
            )
        for i in range(self.cell * self.vertical_cells):
            self.put_pixel(
                self.center_x + self.horizontal_cells * self.cell,
                self.center_y + i,
                *self.vertical_color,
            )

    @staticmethod
    def random_colors():
        list_colors = [
            ((0, 255, 255), (255, 0, 255)),
            ((255, 220, 0), (255, 65, 64)),
            ((46, 204, 113), (52, 152, 219)),
            ((255, 87, 34), (0, 188, 212)),
            ((245, 245, 220), (205, 127, 50)),
            ((0, 255, 255), (255, 0, 255)),
            ((138, 43, 226), (255, 165, 0)),
            ((50, 255, 50), (144, 164, 174)),
            ((255, 128, 171), (128, 222, 234)),
            ((255, 0, 0), (255, 255, 150)),
            ((0, 102, 255), (127, 255, 212)),
        ]
        return random.choice(list_colors)

    def run_win(self):
        self.mlx_instance.mlx_key_hook(self.win_ptr, self.handle_input, vars)
        self.display_maze()
        self.mlx_instance.mlx_loop(self.mlx_ptr)
