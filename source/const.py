from collections import namedtuple


Point = namedtuple('Point', 'x y')

SCREEN_SIZE = (1200, 900)
FPS = 30

CARD_SIZE = (120, 190)
MOVE_SPEED = 40


class Color:
    BLACK = (4, 4, 4)
    YELLOW_BLACK = (250, 240, 190)

    LIGHT_BLACK = (70, 70, 70)
    LIGHTER_BLACK = (30, 30, 30)
    WHITE = (245, 245, 245)
    YELLOW = (255, 211, 38)
    A_BIT_YELLOW_WHITE = (233, 233, 233)
    CHOSEN_WHITE = (245, 180, 180)
    LIGHT_RED = (250, 97, 87)
    GREEN = (60, 180, 60)


class Rank:
    six = '6'
    seven = '7'
    eight = '8'
    nine = '9'
    ten = '10'
    jack = 'jack'
    queen = 'queen'
    king = 'king'
    ace = 'ace'
    back_side = 'back_side'


class Suit:
    hearts = 'hearts'
    diamonds = 'diamonds'
    clubs = 'clubs'
    spades = 'spades'
    back_side = 'back_side'
