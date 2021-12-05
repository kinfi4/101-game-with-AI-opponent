from const import Rank, CARD_SIZE
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

    def was_chosen(self, mouse_pos) -> bool:
        width, height = CARD_SIZE
        x, y = mouse_pos.x, mouse_pos.y
        card_pos_x, card_pos_y = self.sprite.pos

        fits_y = card_pos_y - height // 2 < y < card_pos_y + height // 2
        fits_x = card_pos_x - width // 2 < x < card_pos_x + width // 2

        return fits_x and fits_y

    def __hash__(self):
        return hash(self.rank + self.suit)
