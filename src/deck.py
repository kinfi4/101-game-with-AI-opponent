from random import sample, choice

from src.card import Card
from src.const import Rank, Suit, Point, DECK_POSITION


class Deck:
    def __init__(self):
        self.user_cards = set()
        self.agent_cards = set()
        self.deck_cards = set()
        self.deactivated_cards = set()
        self.card_in_action = None

    def initialize_deck(self):
        self.deck_cards = self._create_all_possible_cards()

        self.agent_cards = set(sample(self.deck_cards, 5))
        self.deck_cards.difference_update(self.agent_cards)

        self.user_cards = set(sample(self.deck_cards, 4))
        self.deck_cards.difference_update(self.user_cards)

        self.card_in_action = self.get_random_card_from_deck()

    def get_random_card_from_deck(self):
        if len(self.deck_cards) == 0:
            self._reshuffle_the_deck()

        random_card = choice(list(self.deck_cards))
        self.deck_cards.difference_update({random_card})

        return random_card

    def _create_all_possible_cards(self):
        suits = [Suit.clubs, Suit.spades, Suit.diamonds, Suit.hearts]
        ranks = [Rank.six, Rank.seven, Rank.eight, Rank.nine, Rank.ten, Rank.jack, Rank.queen, Rank.king, Rank.ace]

        return {self.create_card(DECK_POSITION, suit, rank) for suit in suits for rank in ranks}

    @staticmethod
    def create_card(position: Point, suit, rank):
        return Card(suit=suit, rank=rank, pos_x=position.x, pos_y=position.y)

    def _reshuffle_the_deck(self):
        self.deck_cards = self.deactivated_cards
        self.deactivated_cards = set()

        for card in self.deck_cards:
            card.sprite.pos = DECK_POSITION
