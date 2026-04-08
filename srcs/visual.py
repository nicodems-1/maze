from typing import Any

from mlx.mlx import Mlx
from srcs.maze_generation import generate_maze
import random


class Visual:
    def __init__(self, maze_obj, config):
        self.maze_obj = maze_obj
        self.config = config

        self.mlx_instance = Mlx()
        self.mlx_ptr = self.mlx_instance.mlx_init()

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
        self.padding = 50

        self.key_map = {
            99: self.change_color,
            113: self.close_window,
            114: self.regenerate,
            101: self.dezoom,
            119: self.zoom,
        }

    def handle_input(self, keycode, params):
        func = self.key_map.get(keycode)
        if func:
            func()

    def zoom(self):
        if self.padding > 20:
            self.padding -= 2
        self.display_maze()

    def dezoom(self):
        if self.padding < 120:
            self.padding += 2
        self.display_maze()

    def close_window(self):
        self.mlx_instance.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx_instance.mlx_loop_exit(self.mlx_ptr)

    def change_color(self):
        self.clear_image_buffer()
        self.vertical_color, self.horizontal_color = self.random_colors()
        _, self.log_color = self.random_colors()
        # self.mlx_instance.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.display_maze()

    def regenerate(self):
        self.clear_image_buffer()
        self.maze_obj = generate_maze(self.config)
        self.display_maze()

    def create_window(self):
        _, self.width, self.height = self.mlx_instance.mlx_get_screen_size(
            self.mlx_ptr
        )
        self.win_ptr = self.mlx_instance.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "a-maze-ing"
        )

    def generate_cells(self, hexa, x_offset, y_offset):
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
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.img_ptr,
            self.center_x,
            self.height - (self.center_y // 2),
            0xF54927,
            "Q: quit   C: change colors    R: regenerate",
        )
        self.mlx_instance.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

    def put_pixel(self, x, y, r, g, b):
        index = (y * self.size_line) + (x * (self.bpp // 8))

        self.img_data[index] = b
        self.img_data[index + 1] = g
        self.img_data[index + 2] = r
        self.img_data[index + 3] = 255

    def clear_image_buffer(self):

        black_pixel = bytes([0, 0, 0, 255])

        self.img_data[:] = black_pixel * (self.width * self.height)

    def fill_square(self, offset_x, offset_y):
        for u in range(self.cell):
            for i in range(self.cell):
                self.put_pixel(self.center_x + offset_x + i,
                               self.center_y + offset_y + u,
                               *self.log_color)
            u += 1

    def create_maze(self, parsed: str):

        self.clear_image_buffer()
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


# if __name__ == "__main__":
#     obj = Visual()
#     obj.run_win()
