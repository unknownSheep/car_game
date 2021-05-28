import pygame
import math
import datetime
vec2 = pygame.math.Vector2


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def lines_collide(x1, y1, x2, y2, x3, y3, x4, y4):
    if (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1) == 0:
        return None
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        intersection_x = x1 + (ua * (x2 - x1))
        intersection_y = y1 + (ua * (y2 - y1))
        return vec2(intersection_x, intersection_y)
    return None


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def float_time():
    now_time = datetime.datetime.now().time()
    now_str = str(now_time)
    now_array = now_str.split(':')
    h = float(now_array[0])
    min = float(now_array[1])
    sec = float(now_array[2])
    total = 3600*h + 60*min + sec
    return total
