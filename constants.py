import math
from pygame import Vector2

fps = 60
# substeps = 1

gravity = Vector2(0, 10)
radius_circ = 7
grid_length = radius_circ * 2
width, height = [math.floor(900 / grid_length) * grid_length] * 2
nx_cells = math.floor(width / grid_length)  # Go from 0 to n-1 index
ny_cells = math.floor(height / grid_length)


class CircleSimple:
    def __init__(self, pos, radius, border_width, color):
        self.pos = pos
        self.radius = radius
        self.border_width = border_width
        self.color = color


central_list = [
    CircleSimple((width // 2, height // 2), 220, 15, (150, 150, 150)),
    CircleSimple((width // 2, height // 2), 330, 15, (150, 150, 150)),

]

angle_max = 0.9 + math.pi / 2
angle_min = -0.9 + math.pi / 2

time_loop = 5
speed = 100

XY = Vector2 | tuple[float] | list[float]
