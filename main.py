import pyglet
import game


if __name__ == '__main__':
    print("welcome")
    window = game.Window(1500, 1000, vsync=True, fullscreen=False, resizable=False)
    # window = game.Window(vsync=True, fullscreen=True, resizable=True)
    pyglet.clock.schedule_interval(window.update, 1 / 120)
    pyglet.app.run()
