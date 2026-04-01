from mlx.mlx import Mlx
from typing import Any
import sys
import os
import random


class Visual:
    def __init__(self):
        self.mlx_instance = Mlx()
        self.mlx_ptr = self.mlx_instance.mlx_init()

        self.create_window()

        self.img_ptr = self.mlx_instance.mlx_new_image(
            self.mlx_ptr, self.width, self.height
        )

        self.img_data, self.bpp, self.size_line, self.endian = (
            self.mlx_instance.mlx_get_data_addr(self.img_ptr)
        )

    def close_window(self, keycode, params):
        if keycode == 113:
            self.mlx_instance.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.mlx_instance.mlx_loop_exit(self.mlx_ptr)

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
                    0,
                    255,
                    255,
                )
        # creating column
        if hexa & 8 == 8:
            for i in range(self.cell):
                self.put_pixel(
                    self.center_x + x_offset,
                    self.center_y + i + y_offset,
                    255,
                    0,
                    0,
                )

    def run_win(self):
        self.mlx_instance.mlx_key_hook(self.win_ptr, self.close_window, None)
        self.create_maze(
            "9515391539551795151151153\nEBABAE812853C1412BA812812\n96A8416A84545412AC4282C2A\nC3A83816A9395384453A82D02\n96842A852AC07AAD13A8283C2\nC1296C43AAB83AA92AA8686BA\n92E853968428444682AC12902\nAC3814452FA83FFF82C52C42A\n85684117AFC6857FAC1383D06\nC53AD043AFFFAFFF856AA8143\n91441294297FAFD501142C6BA\nAA912AC3843FAFFF82856D52A\n842A8692A92B8517C4451552A\n816AC384468285293917A9542\nC416928513C443A828456C3BA\n91416AA92C393A82801553AAA\nA81292AA814682C6A8693C6AA\nA8442C6C2C1168552C16A9542\n86956951692C1455416928552\nC545545456C54555545444556"
        )
        self.mlx_instance.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            self.center_x,
            self.height - (self.center_y // 2),
            0xF54927,
            "Q: quit",
        )
        self.mlx_instance.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )
        self.mlx_instance.mlx_loop(self.mlx_ptr)

    def put_pixel(self, x, y, r, g, b):
        index = (y * self.size_line) + (x * (self.bpp // 8))

        self.img_data[index] = b
        self.img_data[index + 1] = g
        self.img_data[index + 2] = r
        self.img_data[index + 3] = 255

    def create_maze(self, parsed: str):
        lines = parsed.split("\n")
        self.horizontal_cells = len(lines[0])
        self.vertical_cells = len(lines)
        self.cell = self.width // (self.vertical_cells + 22)
        self.center_x = int(
            (self.width - (self.cell * self.horizontal_cells)) / 2
        )
        self.center_y = int(
            (self.height - (self.cell * self.vertical_cells)) / 2
        )

        y_offset = -self.cell
        x_offset = 0
        for line in lines:
            x_offset = 0
            y_offset += self.cell
            for letter in line:
                nbr = int(letter, 16)
                self.generate_cells(nbr, x_offset, y_offset)
                x_offset += self.cell
        for i in range(self.cell * len(line)):
            self.put_pixel(
                self.center_x + i,
                self.center_y + len(lines) * self.cell,
                255,
                0,
                0,
            )
        for i in range(self.cell * len(lines)):
            self.put_pixel(
                self.center_x + len(line) * self.cell,
                self.center_y + i,
                0,
                255,
                0,
            )

    @staticmethod
    def random_colors():
        list_colors = [
            ((0, 255, 255), (255, 0, 255)),
            ((255, 220, 0), (255, 65, 64)),
            ((46, 204, 113), (52, 152, 219)),
            ((255, 87, 34), (0, 188, 212)),
            ((245, 245, 220), (205, 127, 50)),
        ]
        return random.choice(list_colors)


if __name__ == "__main__":
    obj = Visual()
    obj.run_win()
