import pygame as pg

from const import FPS, SCREEN_SIZE
from agent import Agent


class GameController:
    def __init__(self):
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.agent = Agent()

        background_image = pg.image.load('./img/board.jpg')
        self.screen.blit(background_image, (0, 0))

        self.cards_group = pg.sprite.Group()

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                self.clock.tick(FPS)
                self.cards_group.update(self.screen)
                pg.display.update()
