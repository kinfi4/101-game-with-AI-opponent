import math

import pygame as pg
from const import MOVE_SPEED, CARD_SIZE


class CardSprite(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, picture_path):
        super().__init__()

        self.image = pg.image.load(picture_path)
        self.image = pg.transform.scale(self.image, CARD_SIZE)
        self.rect = self.image.get_rect()

        self.rect.center = (pos_x, pos_y)
        self.rect.size = CARD_SIZE

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, pos):
        self.rect.center = pos


class SpriteMove:
    def __init__(self, sprites, dest_positions):
        self.sprites = sprites
        self.dest_positions = dest_positions

        for sprite, dest_position in zip(self.sprites, self.dest_positions):
            sprite.start_pos = sprite.pos
            sprite.angle = math.atan2(dest_position[1] - sprite.start_pos[1], dest_position[0] - sprite.start_pos[0])
            sprite.distance = SpriteMove.calc_distance(dest_position, sprite.start_pos)
            sprite.completed = False

    @staticmethod
    def calc_distance(point1, point2):
        return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

    def update(self):
        for sprite, dest_position in zip(self.sprites, self.dest_positions):
            if sprite.completed:
                continue

            new_pos = (sprite.pos[0] + MOVE_SPEED * math.cos(sprite.angle), sprite.pos[1] + MOVE_SPEED * math.sin(sprite.angle))
            distance = SpriteMove.calc_distance(new_pos, sprite.start_pos)

            if distance < sprite.distance:
                sprite.pos = new_pos
            else:
                sprite.pos = dest_position
                sprite.completed = True

    def is_completed(self):
        return all([sprite.completed for sprite in self.sprites])
