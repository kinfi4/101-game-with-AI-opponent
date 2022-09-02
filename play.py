import pygame as pg

from src.controller import GameController

pg.mixer.pre_init(22100, -16, 2, 64)
pg.init()

s = pg.mixer.Sound('./src/sounds/forbidden-sournd.wav')
s.set_volume(0.1)


if __name__ == '__main__':
    game = GameController(sound_controller=s)
    game.main_loop()
