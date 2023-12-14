import pygame as py
import math
from random import choice, uniform, randint
import pygame.time

from circle import Circle, Chain
from constants import *
from calculations import *
from color import ColorLoopingRandom
from grid import Grid
from angle_incrementor import AngleIncr

py.init()

clock = py.time.Clock()
screen = py.display.set_mode((width, height))


def update_pygame(slowdown=1):
    aqua = (0, 150, 255)
    end_points = [(0, 0), (0, width), (width, height), (height, 0)]
    py.draw.polygon(screen, aqua, end_points, 5)

    py.display.update()
    clock.tick(fps / slowdown)


def func1():
    timer = 0
    list_circ: list[Circle] = []
    pos_shoot = (width / 2, height * 1 / 3)

    started = False

    color_circ = ColorLoopingRandom((0, 0, 0), (255, 255, 255), (5, 6, 7), random_mult=2)

    angle = angle_min
    angle_incr = 2 * math.pi / time_loop / fps

    last_time = 0

    add_circles = True
    do_collision_with_central_circ = True

    num_deletions = 0

    grid = Grid()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    exit()
                if event.key == py.K_SPACE:
                    started = True
        time = py.time.get_ticks()
        screen.fill((45, 50, 60))

        timer += 1

        angle += angle_incr
        if angle > angle_max:
            angle_incr = -abs(angle_incr)
        if angle < angle_min:
            angle_incr = abs(angle_incr)

        if timer % 5 == 0:
            color_circ.update()
        if timer % 2 == 0 and add_circles and started:
            vel = py.Vector2((speed * math.cos(angle), speed * math.sin(angle)))
            pos = py.Vector2((width // 4 * math.cos(angle / 16.672)) + width // 2,
                             width // 4 * math.cos(angle * 12.672) + height // 2)
            circ = Circle(pos=pos_shoot, acc=gravity, radius=radius_circ, color=color_circ.get_color())
            circ.set_vel(vel, 1 / (fps))

            list_circ.append(circ)
            grid.add_circ(circ)

        if len(list_circ) >= 240 and False:
            if add_circles is True:
                num_deletions += 1
            add_circles = False
            do_collision_with_central_circ = False

        if add_circles is False:
            if len(list_circ) <= 80:
                add_circles = True
                do_collision_with_central_circ = True

        if started:
            for circ in list_circ:
                circ.move(1 / (fps))

                if do_collision_with_central_circ:
                    temp_circ = central_list[0]
                    circ.constraint_half_circle(temp_circ.pos, temp_circ.radius, temp_circ.border_width, False)

                    temp_circ = central_list[1]
                    circ.constraint_half_circle(temp_circ.pos, temp_circ.radius, temp_circ.border_width, True)
            grid.do_collision()

            new_list_circ = []

            for circ in list_circ:
                if circ.within_bounds():
                    new_list_circ.append(circ)
            if timer % 60 == 0:
                print(len(list_circ), grid.amount_looped)

            list_circ = new_list_circ
            grid.reset_to_circ_list(list_circ)

            for circ in list_circ:
                circ.draw(screen)

            if do_collision_with_central_circ:
                temp_circ = central_list[0]
                py.draw.circle(screen, temp_circ.color, temp_circ.pos, temp_circ.radius + temp_circ.border_width,
                               width=temp_circ.border_width,
                               draw_bottom_left=True, draw_bottom_right=True)
                temp_circ = central_list[1]
                py.draw.circle(screen, temp_circ.color, temp_circ.pos, temp_circ.radius + temp_circ.border_width,
                               width=temp_circ.border_width,
                               draw_top_left=True, draw_top_right=True)
        if timer % 60 == 0:
            print((pygame.time.get_ticks() - time) * 60 / 1000)

        update_pygame()


def func2():
    started = False

    chain = Chain(1.2, 300, (width * 0.2, height * .6), (width * .8, height * .6), 1 * gravity, 5)
    grid = Grid()

    circ_list: list[Circle] = []

    timer = 0

    pos_shoot1 = Vector2((width * (2 / 4), height * 0.2))
    angle_min = angle_between(chain.pos_start, pos_shoot1)
    angle_max = angle_between(chain.pos_end, pos_shoot1)

    angle_incr = AngleIncr(angle_min, angle_max, 0.05)
    color_circ = ColorLoopingRandom((0, 0, 0), (255, 255, 255), (5, 6, 7), random_mult=2)

    while True:
        timer += 1
        screen.fill((0, 0, 0))
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    exit()
                if event.key == py.K_SPACE:
                    started = True
        if started:
            angle_incr.update()
            chain.move(1 / fps)
            color_circ.update()

            if timer % 3 == 0:
                angle = angle_incr.angle
                circ = Circle(pos_shoot1, gravity * 1, radius_circ, color_circ.color_current)
                circ.set_vel(vec(200, angle), 1 / fps)
                circ_list.append(circ)

            sub = 20
            for i in range(sub):
                chain.collide_within()
            chain.draw(screen)
            for circ in circ_list:
                circ.move(1 / fps)
            new_list_circ = []

            for circ in circ_list:
                if circ.within_bounds():
                    new_list_circ.append(circ)
            circ_list = new_list_circ
            for circ in circ_list:
                circ.draw(screen)

            grid.reset_to_circ_list(circ_list)
            chain.add_to_grid(grid)

            grid.do_collision()

        update_pygame(1)

        if timer % 60 == 0:
            print(timer)


def check_exit():
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                exit()


def ex_1():
    timer = 0

    while True:
        timer += 1
        screen.fill((0, 0, 0))
        check_exit()

        update_pygame(1)


def ex_2():
    while True:
        screen.fill((0, 0, 0))
        check_exit()
        py.draw.circle(screen, (255, 255, 255), (width // 2, height // 2), 50)
        update_pygame(1)


class CircleEx3:
    pos: Vector2

    def __init__(self):
        self.pos = Vector2(50, 50)

    def move(self):
        self.pos += Vector2(2, 3)

    def draw(self):
        py.draw.circle(screen, (255, 255, 255), self.pos, 50)


def ex_3():
    circ = CircleEx3()
    while True:
        screen.fill((0, 0, 0))
        check_exit()

        circ.move()
        circ.draw()

        py.display.update()
        clock.tick(fps)  # fps= 60


class CircleEx4:
    pos: Vector2
    past_pos: Vector2

    def __init__(self):
        self.pos = Vector2(50, 50)
        self.past_pos = self.pos.copy() - Vector2(5, 0)

    def move(self, dt):
        gravity_ = Vector2(0, 300)

        new_pos = 2 * self.pos - self.past_pos + gravity_ * dt ** 2
        self.past_pos = self.pos.copy()
        self.pos = new_pos

    def draw(self):
        py.draw.circle(screen, (255, 255, 255), self.pos, 50)


def ex_4():
    circ = CircleEx4()
    while True:
        screen.fill((0, 0, 0))
        check_exit()

        circ.move(1 / fps)
        circ.draw()

        py.display.update()
        clock.tick(fps)  # fps= 60


class CircleEx5:
    pos: Vector2
    past_pos: Vector2
    radius: float

    def __init__(self):
        self.pos = Vector2(width // 2, 50)
        self.past_pos = self.pos.copy() - Vector2(5, 0)
        self.radius = 20

    def move(self, dt):
        gravity_ = Vector2(0, 100)

        new_pos = 2 * self.pos - self.past_pos + gravity_ * dt ** 2
        self.past_pos = self.pos.copy()
        self.pos = new_pos

    def constraint_inside_circle(self, pos: XY, radius: float):
        d = dist(self.pos, pos)
        if d > radius - self.radius:
            self.pos = pos + (self.pos - pos) * (radius - self.radius) / d

    def draw(self):
        py.draw.circle(screen, (255, 255, 255), self.pos, self.radius)


center = Vector2(width // 2, height // 2)


def ex_5():
    circ = CircleEx5()
    while True:
        screen.fill((0, 0, 0))
        check_exit()

        circ.move(1 / fps)
        circ.draw()

        circ.constraint_inside_circle(center, 350)
        py.draw.circle(screen, 'Blue', center, 350, 5)

        py.display.update()
        clock.tick(fps)  # fps= 60


class CircleEx6:
    pos: Vector2
    past_pos: Vector2
    radius: float

    def __init__(self):
        self.pos = Vector2(width // 2, 50)
        self.past_pos = self.pos.copy() - Vector2(5 * math.cos(uniform(0, 10)), 5 * math.sin(uniform(0, 10)))
        self.radius = 20

    def move(self, dt):
        gravity_ = Vector2(0, 100)

        new_pos = 2 * self.pos - self.past_pos + gravity_ * dt ** 2
        self.past_pos = self.pos.copy()
        self.pos = new_pos

    def constraint_inside_circle(self, pos: XY, radius: float):
        d = dist(self.pos, pos)
        if d > radius - self.radius:
            self.pos = pos + (self.pos - pos) * (radius - self.radius) / d

    def draw(self):
        py.draw.circle(screen, (255, 255, 255), self.pos, self.radius)


def ex_6():
    circ_list = [CircleEx6() for _ in range(50)]

    while True:

        screen.fill((0, 0, 0))
        check_exit()

        for circ in circ_list:
            circ.move(1 / fps)
            circ.draw()

            circ.constraint_inside_circle(center, 350)
        py.draw.circle(screen, 'Blue', center, 350, 5)

        py.display.update()
        clock.tick(fps)  # fps= 60


class CircleEx7:
    pos: Vector2
    past_pos: Vector2
    radius: float

    def __init__(self):
        self.pos = Vector2(width // 2, 50)
        self.past_pos = self.pos.copy() - Vector2(5 * math.cos(uniform(0, 10)), 5 * math.sin(uniform(0, 10)))
        self.radius = 20

    def move(self, dt):
        gravity_ = Vector2(0, 100)

        new_pos = 2 * self.pos - self.past_pos + gravity_ * dt ** 2
        self.past_pos = self.pos.copy()
        self.pos = new_pos

    def constraint_inside_circle(self, pos: XY, radius: float):
        d = dist(self.pos, pos)
        if d > radius - self.radius:
            self.pos = pos + (self.pos - pos) * (radius - self.radius) / d

    def draw(self):
        py.draw.circle(screen, (255, 255, 255), self.pos, self.radius)

    def collision(self, circ):
        d = dist(self.pos, circ.pos)

        if d < self.radius + circ.radius:
            adjustment = (-d + (self.radius + circ.radius))

            diff = self.pos - circ.pos
            mag_diff = diff.magnitude()

            self.pos += diff * adjustment * 1 / 2 / mag_diff
            circ.pos -= diff * adjustment * 1 / 2 / mag_diff


def ex_7():
    circ_templates = [CircleEx7() for _ in range(5000)]

    circ_list = []
    timer = 0
    while True:
        timer += 1
        screen.fill((0, 0, 0))
        check_exit()

        if timer % 3 == 0:
            circ_list.append(circ_templates[(timer // 10)])

        for circ in circ_list:
            circ.move(1 / fps)
            circ.draw()

            circ.constraint_inside_circle(center, 350)

            for other_circ in circ_list:
                if circ is not other_circ:
                    circ.collision(other_circ)

        py.draw.circle(screen, 'Blue', center, 350, 5)

        py.display.update()
        clock.tick(fps)  # fps= 60


func2()
