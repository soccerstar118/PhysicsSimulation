import math
import pygame


def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def angle_between(pos1, pos2):
    return math.atan2(pos1[1] - pos2[1], pos1[0] - pos2[0])


def vec(radius, angle):
    return pygame.Vector2(radius * math.cos(angle), radius * math.sin(angle))
