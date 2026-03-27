import pygame as py
import sys

class Game:
    def __init__(self):
        py.init()
        py.display.set_caption("My First Pygame Game")
        self.screen = py.display.set_mode((800, 600))

        self.clock = py.time.Clock()

        self.img = py.image.load('')

    def run(self):
        running = True
        while running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                    py.quit()
                    sys.exit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        running = False
            py.display.update()
            self.clock.tick(60)
            self.screen.fill((128, 0, 128))

Game().run()