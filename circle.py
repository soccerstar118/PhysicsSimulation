from __future__ import annotations

import pygame as py
from pygame import Vector2, Vector3
import random
import math
from constants import width, height, XY
from calculations import *

Color = Vector3 | tuple | list

chain_const = 10 ** 5 + 23423


def circle_surf(radius, color, border_length=0):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius, border_length)
    # surf.set_colorkey((0, 0, 0))
    return surf


def col_mult(arr, mult, *, max_=float('inf')):
    temp_arr = [num * mult for num in arr]
    for i in range(len(temp_arr)):
        if max_ < temp_arr[i]:
            temp_arr[i] = max_
    return temp_arr


def col_mult_half(arr, *, max_=float('inf')):
    return col_mult(arr, 0.5, max_=max_)


class Circle:
    def __init__(self, pos: XY, acc: XY, radius: float, color: Color = None, id_type=0, pulsate_mult=2.6,
                 border_length=0):
        """
        :param id: leave at None to not include. Circles of same (non-None) id do not collide with each other
        """
        if color is None:
            color = (255, 255, 255)

        self.id = id_type

        self.pos = Vector2(pos)

        self.past_pos = self.pos.copy()

        self.acc = Vector2(acc)
        self.radius = radius
        self.color = Vector3(color)

        self.past_grid_position = (None, None)

        self.mass = self.radius ** 2
        self.timer = 0

        self.border_length = 5  # border_length
        self.pulsate_mult = pulsate_mult
        self.current_pulsate_mult = pulsate_mult
        self.pulsate_mult_add_subtract = -1
        self.circle_glow = col_mult_half(self.color)

    def move(self, dt):
        new_pos = 2 * self.pos - self.past_pos + self.acc * dt ** 2

        self.past_pos = self.pos
        self.pos = new_pos

        self.timer += 1

    def draw(self, screen, fancy=True):
        if fancy:
            py.draw.circle(screen, self.color, self.pos, self.radius, self.border_length)

            self.current_pulsate_mult += self.pulsate_mult / 300 * self.pulsate_mult_add_subtract
            if self.current_pulsate_mult > self.pulsate_mult:
                self.pulsate_mult_add_subtract = -1
            elif self.current_pulsate_mult < 0.5 + self.pulsate_mult / 2:
                self.pulsate_mult_add_subtract = 1
            screen.blit(circle_surf(self.radius * self.current_pulsate_mult, self.circle_glow, self.border_length),
                        (self.pos.x - self.radius - (self.current_pulsate_mult - 1) * self.radius,
                         self.pos.y - self.radius - (self.current_pulsate_mult - 1) * self.radius),
                        special_flags=pygame.BLEND_RGB_ADD)
        py.draw.circle(screen, self.color, self.pos, self.radius)

    def constraint_inside_circle(self, pos: XY, radius: float):
        d = dist(self.pos, pos)
        if d > radius - self.radius:
            self.pos = pos + (self.pos - pos) * (radius - self.radius) / d

    def constraint_half_circle(self, pos: XY, radius, border_width, top_half: bool):
        if top_half:
            if self.pos.y < pos[1]:
                d = dist(self.pos, pos)
                if d > radius - self.radius and not (d - self.radius > radius + border_width):
                    self.pos = pos + (self.pos - pos) * (radius - self.radius) / d
        else:
            if self.pos.y > pos[1]:
                d = dist(self.pos, pos)
                if d > radius - self.radius and not (d - self.radius > radius + border_width):
                    self.pos = pos + (self.pos - pos) * (radius - self.radius) / d

    def collision(self, circ: Circle, massless_collision=False):
        if self.id != 0:
            if self.id == circ.id:
                return

        d = dist(self.pos, circ.pos)

        if d < self.radius + circ.radius:
            adjustment = (-d + (self.radius + circ.radius))

            diff = self.pos - circ.pos
            mag_diff = diff.magnitude()

            if not massless_collision:
                self.pos += diff * adjustment * circ.mass / (self.mass + circ.mass) / mag_diff
                circ.pos -= diff * adjustment * self.mass / (circ.mass + self.mass) / mag_diff
            else:
                self.pos += diff * adjustment * 1 / 2 / mag_diff
                circ.pos -= diff * adjustment * 1 / 2 / mag_diff

    def get_vel(self, dt):
        return (self.pos - self.past_pos) / dt

    def set_vel(self, vel: XY, dt):
        self.past_pos = self.pos - Vector2(vel) * dt

    def within_bounds(self) -> bool:
        if self.pos.x - self.radius <= 0:
            return False
        if self.pos.y - self.radius <= 0:
            return False
        if self.pos.x + self.radius >= width:
            return False
        if self.pos.y + self.radius >= height:
            return False
        return True

    def add_to_grid(self, grid):
        grid.add_circ(self)


class Chain:
    def __init__(self, flexibility: float, circ_amount, pos_start, pos_end: XY, acc: XY, radius, color=None):
        """
        :param flexibility: Must be from 1...infinity. The target distance is directly correlational with flexibility.
        """
        global chain_const
        self.pos_start = Vector2(pos_start)
        self.pos_end = Vector2(pos_end)
        self.circ_amount = circ_amount
        self.circ_list: list[Circle] = [
            Circle(self.pos_start + (self.pos_end - self.pos_start) * i / (circ_amount - 1), acc, radius, color,
                   id_type=chain_const)
            for i in range(circ_amount)]
        chain_const += 1

        self.target_distance = dist(self.pos_start, self.pos_end) / self.circ_amount * flexibility

    def move(self, dt):
        for circ in self.circ_list:
            circ.move(dt)

    def collide_within(self):
        for i in range(self.circ_amount - 1):
            circ1 = self.circ_list[i]
            circ2 = self.circ_list[i + 1]

            pos1 = circ1.pos
            pos2 = circ2.pos

            axis = pos1 - pos2

            n = axis / dist(pos1, pos2)

            delt = self.target_distance - dist(pos1, pos2)

            circ1.pos = pos1 + 0.5 * delt * n
            circ2.pos = pos2 - 0.5 * delt * n

        self.circ_list[0].pos = self.pos_start.copy()
        self.circ_list[-1].pos = self.pos_end.copy()

    def draw(self, screen):
        for circ in self.circ_list:
            circ.draw(screen)

    def constraint_inside_circle(self, pos: XY, radius: float):
        for circ in self.circ_list:
            circ.constraint_inside_circle(pos, radius)

    def constraint_half_circle(self, pos: XY, radius, border_width, top_half: bool):
        for circ in self.circ_list:
            circ.constraint_half_circle(pos, radius, border_width, top_half)

    def collision(self, other_circ: Circle):
        for circ in self.circ_list:
            circ.collision(other_circ)

    def add_to_grid(self, grid):
        for circ in self.circ_list:
            circ.add_to_grid(grid)
