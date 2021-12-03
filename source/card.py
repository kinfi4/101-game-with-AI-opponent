from const import Rank
from card_sprite import CardSprite


class Card:
    def __init__(self, pos_x, pos_y, rank, suit):
        self.position_x = pos_x
        self.position_y = pos_y
        self.rank = rank
        self.suit = suit

        if rank == Rank.back_side:
            picture_path = './img/back-side.png'
        else:
            picture_path = f'./img/cards/{rank}_of_{suit}.png'

        self.sprite = CardSprite(self.position_x, self.position_y, picture_path)

    def __hash__(self):
        return hash(self.rank + self.suit)
