from random import sample, choice

import pygame as pg

from const import FPS, SCREEN_SIZE, Point, Suit, Rank
from agent import Agent
from card import Card
from card_sprite import SpriteMove


class GameController:
    def __init__(self):
        self.deck_position = (1000, 395)
        self.table_center = (500, 395)

        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.agent = Agent()

        self.background_image = pg.image.load('./img/board.jpg')
        self.screen.blit(self.background_image, (0, 0))

        self.user_cards = set()
        self.agent_cards = set()
        self.deck_cards = set()
        self.card_in_action = None

        self.deck_card_sprite_group = pg.sprite.Group([self.create_card(Point(*self.deck_position), Suit.back_side, Rank.back_side).sprite])
        self.card_in_action_sprite_group = pg.sprite.Group([])
        self.user_cards_sprites = pg.sprite.Group([])
        self.agent_cards_sprites = pg.sprite.Group([])

        self.sprite_moves = []

        self.initialize_board()

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                self.clock.tick(FPS)

                for move in self.sprite_moves:
                    move.update()

                    if move.is_completed():
                        self.sprite_moves.remove(move)

                self.screen.blit(self.background_image, (0, 0))

                self.deck_card_sprite_group.draw(self.screen)
                self.card_in_action_sprite_group.draw(self.screen)
                self.agent_cards_sprites.draw(self.screen)
                self.user_cards_sprites.draw(self.screen)
                pg.display.update()

    def initialize_board(self):
        self.deck_cards = self.create_all_cards()

        self.agent_cards = set(sample(self.deck_cards, 5))
        self.deck_cards.difference_update(self.agent_cards)
        self.agent_cards_sprites.add([c.sprite for c in self.agent_cards])

        self.user_cards = set(sample(self.deck_cards, 4))
        self.deck_cards.difference_update(self.user_cards)
        self.user_cards_sprites.add([c.sprite for c in self.user_cards])

        self.card_in_action = self.get_random_card_from_deck()
        self.card_in_action_sprite_group.add(self.card_in_action.sprite)

        self.sprite_moves.append(SpriteMove([self.card_in_action.sprite], [self.table_center]))

    def get_random_card_from_deck(self):
        random_card = choice(list(self.deck_cards))
        self.deck_cards.difference_update({random_card})

        return random_card

    def create_all_cards(self):
        suits = [Suit.clubs, Suit.spades, Suit.diamonds, Suit.hearts]
        ranks = [Rank.six, Rank.seven, Rank.eight, Rank.nine, Rank.ten, Rank.jack, Rank.queen, Rank.king, Rank.ace]

        list_of_cards = {self.create_card(Point(*self.deck_position), suit, rank) for suit in suits for rank in ranks}

        return list_of_cards

    def can_make_move(self, chosen_card: Card):
        return self.card_in_action is None \
               or self.card_in_action.suit == chosen_card.suit \
               or self.card_in_action.rank == chosen_card.rank

    @staticmethod
    def create_card(position: Point, suit, rank):
        return Card(suit=suit, rank=rank, pos_x=position.x, pos_y=position.y)
