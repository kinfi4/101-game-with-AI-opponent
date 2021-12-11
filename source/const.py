from collections import namedtuple

USER = 'USER'
AGENT = 'AGENT'

Point = namedtuple('Point', 'x y')

SCREEN_SIZE = (1900, 900)
FPS = 100

CARD_SIZE = (120, 190)

DECK_POSITION = Point(1000, 395)
TABLE_CENTER = Point(500, 395)


def change_card_size(multiplier):
    global CARD_SIZE
    CARD_SIZE = CARD_SIZE[0]*multiplier, CARD_SIZE[1]*multiplier


MOVE_SPEED = 15


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


CARDS_POINTS_BY_RANK = {
    Rank.six: 0,
    Rank.seven: 50,
    Rank.eight: 25,
    Rank.nine: 0,
    Rank.ten: 10,
    Rank.jack: 20,
    Rank.queen: 0,
    Rank.king: 0,
    Rank.ace: 25
}
