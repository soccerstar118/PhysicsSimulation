from constants import grid_length, XY, nx_cells, ny_cells
import math
from circle import Circle, Chain


class Grid:
    def __init__(self):
        self.grid: list[list[list[Circle]]] = [[[] for _ in range(ny_cells)] for _ in range(nx_cells)]

        self.amount_looped = 0

    def add_circ(self, circ: Circle):
        x, y = circ.pos
        adj_x = math.floor(x / grid_length)
        adj_y = math.floor(y / grid_length)

        if 0 <= adj_x < nx_cells and 0 <= adj_y < ny_cells:
            self.grid[adj_x][adj_y].append(circ)

    def reset_to_circ_list(self, circ_list: list[Circle]):
        self.grid: list[list[list[Circle]]] = [[[] for _ in range(ny_cells)] for _ in range(nx_cells)]
        for circ in circ_list:
            self.add_circ(circ)

    def do_collision(self):
        for i in range(nx_cells):
            for j in range(ny_cells):
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if 0 <= i + di < nx_cells and 0 <= j + dj < ny_cells:
                            for circ1 in self.grid[i][j]:
                                for circ2 in self.grid[i + di][j + dj]:
                                    if circ1 is not circ2:
                                        circ1.collision(circ2)
                                    self.amount_looped += 1
