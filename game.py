import pyglet
import pygame
import utils
import car

pyglet.resource.path = ['assets']
pyglet.resource.reindex()
vec2 = pygame.math.Vector2
reference_vec = vec2(0, 1)

car_image = pyglet.resource.image("car.png")
utils.center_image(car_image)


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()

        self.fps_display = pyglet.window.FPSDisplay(window=self)
        self.fps_display.label.x = 0
        self.fps_display.label.y = self.height - 15
        self.fps_display.label.color = (255, 255, 255, 255)
        self.fps_display.label.font_size = 11

        self.car = car.Car(img=car_image, x=172, y=872, batch=self.batch)
        self.walls, self.gates = self.generate_terrain()

    def generate_terrain(self):
        walls = []
        gates = []
        map_file = open("assets/terrain.map")
        gates_file = open("assets/gates.map")
        while True:
            points_co_str = map_file.readline().strip()
            if not points_co_str:
                break
            points_co_str_array = points_co_str.split('/')
            points_co = []
            for co in points_co_str_array:
                points_co.append(float(co))
            line = pyglet.shapes.Line(points_co[0], points_co[1], points_co[2], points_co[3],
                                      10, color=(128, 128, 128), batch=self.batch)
            walls.append(line)
        while True:
            points_co_str = gates_file.readline().strip()
            if not points_co_str:
                break
            points_co_str_array = points_co_str.split('/')
            points_co = []
            for co in points_co_str_array:
                points_co.append(float(co))
            line = pyglet.shapes.Line(points_co[0], points_co[1], points_co[2], points_co[3],
                                      10, color=(50, 50, 255), batch=self.batch)
            gates.append(line)

        return walls, gates

    def update(self, dt):
        self.car.move()
        self.detect_collisions()
        # self.detect_wall_distances()
        # print(self.detect_wall_distances())

    def detect_collisions(self):
        right_vec = vec2(self.car.direction.y, self.car.direction.x)
        up_vec = vec2(self.car.direction.y, self.car.direction.x).rotate(-90)
        car_corners = []
        corner_multipliers = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
        car_pos = vec2(self.car.x, self.car.y)

        for i in range(0, 4):
            car_corners.append(car_pos + (right_vec * self.car.width / 2 * corner_multipliers[i][1]) +
                               (up_vec * self.car.height / 2 * corner_multipliers[i][0]))

        for i in range(0, 4):
            j = i + 1
            j = j % 4
            # line = pyglet.shapes.Line(car_corners[i].x, car_corners[i].y, car_corners[j].x, car_corners[j].y,
            #                           10, color=(0, 128, 0), batch=self.batch)
            # self.car.hitbox[i] = line # uncomment to see the hit-box
            if utils.lines_collide(car_corners[i].x, car_corners[i].y, car_corners[j].x, car_corners[j].y,
                                   self.gates[self.car.next_gate].x, self.gates[self.car.next_gate].y,
                                   self.gates[self.car.next_gate].x2, self.gates[self.car.next_gate].y2):
                self.car.next_gate += 1
                self.car.score += 1
                # delta_t = utils.float_time() - self.car.arrival_time
                # if delta_t != 0:
                #     self.car.score += 3/delta_t
                # self.car.arrival_time = utils.float_time()

                print("score : {}".format(self.car.score))
                if self.car.next_gate == (len(self.gates)):
                    self.car.next_gate = 0

            for wall in self.walls:
                if utils.lines_collide(wall.x, wall.y, wall.x2, wall.y2,
                                       car_corners[i].x, car_corners[i].y, car_corners[j].x, car_corners[j].y):
                    # self.car.dead = True
                    # self.car.reset()
                    self.car.score -= 2
                    self.reset()
                    # print("ouch")

    def detect_wall_distances(self):
        distances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        rotation_angles = [0, 180, 22.5, -22.5, 45, -45, 67, -67, 90, -90]
        player_pos_vec = vec2(self.car.y, self.car.x)
        i = 0
        for a in rotation_angles:
            line_vec = self.car.direction.rotate(a) * 150 + player_pos_vec
            line = pyglet.shapes.Line(self.car.x, self.car.y, line_vec.y, line_vec.x, 2, color=(86, 86, 86),
                                      batch=self.batch)
            self.car.antennas[i] = line
            i += 1

        c = 0
        for a in self.car.antennas:
            for w in self.walls:
                collision = utils.lines_collide(w.x, w.y, w.x2, w.y2, a.x, a.y, a.x2, a.y2)
                if collision:
                    self.car.collision_points[c] = pyglet.shapes.Circle(collision.x, collision.y,
                                                                        10, color=(255, 255, 255), batch=self.batch)
                distances[c] = utils.dist(self.car.collision_points[c].x, self.car.collision_points[c].y,
                                          self.car.x, self.car.y)
            c += 1
        # return distances

    def reset(self):
        self.car.reset()

    def on_mouse_press(self, x, y, button, modifiers):
        print(self.car.x, self.car.y)

    def on_draw(self):
        self.clear()
        self.fps_display.draw()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            self.car.keys['left'] = True
        elif symbol == pyglet.window.key.D:
            self.car.keys['right'] = True
        elif symbol == pyglet.window.key.Z:
            self.car.keys['forward'] = True
        elif symbol == pyglet.window.key.S:
            self.car.keys['backward'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            self.car.keys['left'] = False
        elif symbol == pyglet.window.key.D:
            self.car.keys['right'] = False
        elif symbol == pyglet.window.key.Z:
            self.car.keys['forward'] = False
        elif symbol == pyglet.window.key.S:
            self.car.keys['backward'] = False
