import pyglet
import pygame
import os
vec2 = pygame.math.Vector2

# os.remove("assets/terrain.map")
# os.remove("assets/gates.map")


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lines = []
        self.batch = pyglet.graphics.Batch()
        self.begin = vec2(0, 0)
        self.end = vec2(0, 0)

        self.terrain_file = open("assets/terrain.map", "a")
        self.gates_file = open("assets/gates.map", "a")

    def on_mouse_press(self, x, y, button, modifiers):
        pos = vec2(x, y)
        self.begin = pos
        print("position debut :", pos)

    def on_mouse_release(self, x, y, button, modifiers):
        pos = vec2(x, y)
        self.end = pos
        print("position fin :", pos)

        if button == 1:
            print(button)
            line = pyglet.shapes.Line(self.begin.x, self.begin.y, self.end.x, self.end.y, 10, color=(128, 128, 128), batch=self.batch)
            self.lines.append(line)
            self.terrain_file.write(str(self.begin.x) + "/" + str(self.begin.y) + "/" + str(self.end.x) + "/" + str(self.end.y) + "\n")
        elif button == 4:
            line = pyglet.shapes.Line(self.begin.x, self.begin.y, self.end.x, self.end.y, 10, color=(0, 0, 255), batch=self.batch)
            self.lines.append(line)
            self.gates_file.write(str(self.begin.x) + "/" + str(self.begin.y) + "/" + str(self.end.x) + "/" + str(self.end.y) + "\n")

    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == '__main__':
    window = Window(1500, 1000, vsync=True, fullscreen=False)
    # window = Window(vsync=True, fullscreen=True)
    pyglet.app.run()
