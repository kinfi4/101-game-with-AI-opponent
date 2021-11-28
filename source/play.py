import pygame as pg

from controller import GameController

pg.init()


if __name__ == '__main__':
    game = GameController()
    game.main_loop()
