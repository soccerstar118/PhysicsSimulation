import pygame as py
import random


def get_into_color_range(color: py.Vector3 | tuple) -> py.Vector3:
    color = py.Vector3(color)
    for i in range(3):
        if color[i] < 0:
            color[i] = 0
        if color[i] > 255:
            color[i] = 255
    return color


class ColorStableDecaying:
    def __init__(self, color_start: tuple | py.Vector3, color_end: tuple | py.Vector3,
                 frames_until_reaching_end_color: int):
        color_start = get_into_color_range(color_start)
        color_end = get_into_color_range(color_end)

        self.frames_until_reaching_end_color = frames_until_reaching_end_color

        self.color_incr = (color_end - color_start) / self.frames_until_reaching_end_color
        self.color_current = color_start
        self.current_time = 0

    def update_color_reached_end(self) -> bool:
        self.current_time += 1

        if self.current_time < self.frames_until_reaching_end_color:
            self.color_current += self.color_incr
            self.color_current = get_into_color_range(self.color_current)
            return False
        return True

    def __iter__(self):
        for i in range(3):
            yield int(self.color_current[i])


class ColorLoopingRandom:
    def __init__(self, color_low: tuple | py.Vector3, color_high: tuple | py.Vector3, color_incr: tuple | py.Vector3, *,
                 random_mult: float = 0, color_start=None):
        self.color_low = py.Vector3(color_low)
        self.color_high = py.Vector3(color_high)

        self.original_color_incr = py.Vector3(color_incr)
        self.current_color_incr = py.Vector3(color_incr)

        self.random_mult = random_mult  # defaulted to 0 for no randomization

        if color_start is None:
            self.color_current = py.Vector3(color_low)
        else:
            self.color_current = py.Vector3(color_start)

    def update(self) -> None:
        for i in range(3):
            self.color_current[i] += self.current_color_incr[i]
            if self.color_current[i] >= self.color_high[i]:
                self.color_current[i] = self.color_high[i]
                self.current_color_incr[i] = -abs(self.original_color_incr[i]) * random.uniform(1 - self.random_mult,
                                                                                                1 + self.random_mult)
            if self.color_current[i] <= self.color_low[i]:
                self.color_current[i] = self.color_low[i]
                self.current_color_incr[i] = abs(self.original_color_incr[i]) * random.uniform(1 - self.random_mult,
                                                                                               1 + self.random_mult)

    def get_color(self):
        return py.Vector3(self.color_current)

    def __iter__(self):
        for i in range(3):
            yield int(self.color_current[i])

# class ColorLoopingStable:
#     def __init__(self, color_start: tuple | py.Vector3, color_end: tuple | py.Vector3, time_spend):
#         raise Exception
#         pass
