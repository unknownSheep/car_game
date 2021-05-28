import pyglet
import pygame
import utils

vec2 = pygame.math.Vector2
reference_vec = vec2(0, 1)


class Car (pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(rotation=0, scale_x=70/self.width, scale_y=35/self.height)

        self.next_gate = 0
        self.arrival_time = utils.float_time()
        self.score = 0
        self.dead = False

        self.vel = 0
        self.hitbox = []
        for i in range(0, 4):
            line = pyglet.shapes.Line(0, 0, 0, 0, 10, color=(128, 128, 128))
            self.hitbox.append(line)

        self.antennas = []
        for i in range(0, 10):
            line = pyglet.shapes.Line(0, 0, 0, 0, 10, color=(128, 128, 128))
            self.antennas.append(line)

        self.collision_points = []
        for i in range(0, 10):
            point = pyglet.shapes.Circle(0, 0, 10, segments=None, color=(255, 255, 255))
            self.collision_points.append(point)

        self.friction = 0.98

        self.acceleration = 0
        self.acceleration_rate = self.width / 160.0

        self.direction = vec2(0, 1)
        self.direction_rate = 4

        self.keys = dict(left=False, right=False, forward=False, backward=False)

    def move(self):
        if self.keys['forward']:
            self.acceleration = self.acceleration_rate
        elif self.keys['backward']:
            self.acceleration = -self.acceleration_rate
        else:
            self.acceleration = 0

        if self.keys['left']:
            self.direction = self.direction.rotate(-self.direction_rate)
            self.update(rotation=-self.direction.angle_to(reference_vec))
        elif self.keys['right']:
            self.direction = self.direction.rotate(self.direction_rate)
            self.update(rotation=-self.direction.angle_to(reference_vec))

        self.vel += self.acceleration
        self.vel *= self.friction

        self.direction_rate = 0.8 * self.vel
        if self.direction_rate >= 4:
            self.direction_rate = 4

        self.x += self.vel * self.direction.y
        self.y += self.vel * self.direction.x
