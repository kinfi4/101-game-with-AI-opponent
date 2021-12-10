import math
from random import sample, choice

import pygame as pg

from card import Card
from card_sprite import SpriteMove
from const import FPS, SCREEN_SIZE, Point, Suit, Rank, Color, AGENT, USER, CARD_SIZE, CARDS_POINTS_BY_RANK


class GameController:
    def __init__(self, sound_controller=None):
        self.sound_controller = sound_controller

        self.deck_position = Point(1000, 395)
        self.table_center = Point(500, 395)

        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()

        self.background_image = pg.image.load('./img/board.jpg')
        self.screen.blit(self.background_image, (0, 0))

        self.user_cards = set()
        self.agent_cards = set()
        self.deck_cards = set()
        self.deactivated_cards = set()
        self.card_in_action = None

        self.deck_card_sprite_group = pg.sprite.Group([self.create_card(Point(*self.deck_position), Suit.back_side, Rank.back_side).sprite])
        self.card_in_action_sprite_group = pg.sprite.Group([])
        self.user_cards_sprites = pg.sprite.Group([])
        self.agent_cards_sprites = pg.sprite.Group([])

        self.sprite_moves = []
        self.current_player_move = USER
        self.game_is_over = False
        self.is_animating = True

        self.show_skip_button = True
        self.skip_button_pos = Point(100, 395)

        self.can_through_only_by_rank = True

        self.can_get_new_card = False
        self.six_in_action = False

        self._initialize_board()

    def main_loop(self):
        while True:
            self._check_if_game_is_over()
            self.is_animating = len(self.sprite_moves) != 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif not self.is_animating and event.type == pg.MOUSEBUTTONDOWN:
                    self._check_user_input()

            if self.game_is_over:
                continue

            if not self.is_animating and self.current_player_move == AGENT and not self.can_through_only_by_rank:
                self._ai_decide_which_move_to_make()
            elif not self.is_animating and self.current_player_move == AGENT:
                self._ai_through_all_possible_cards()

            self._update_animation()

            self.screen.blit(self.background_image, (0, 0))

            self.deck_card_sprite_group.draw(self.screen)
            self.card_in_action_sprite_group.draw(self.screen)
            self.agent_cards_sprites.draw(self.screen)
            self.user_cards_sprites.draw(self.screen)

            if self.show_skip_button:
                self._render_skip_button()

            pg.display.update()
            self.clock.tick(FPS)

    def _check_user_input(self):
        rel = pg.mouse.get_rel()
        if math.fabs(rel[0]) < 1 and math.fabs(rel[1]) < 1:
            return

        if self.current_player_move == USER:
            mouse_pos = Point(*pg.mouse.get_pos())

            if self.can_get_new_card and self._user_has_chosen_deck(mouse_pos):
                self._player_gets_a_card(USER)

                if not self.six_in_action:
                    self.can_get_new_card = False
                    self.show_skip_button = True
            elif 700 < mouse_pos.y < 1000:
                for user_card in self.user_cards:
                    if user_card.was_chosen(mouse_pos):
                        if self.can_make_move(user_card):
                            self._make_a_move(user_card)
                            break
                        else:
                            self.sound_controller.play(0, 0, fade_ms=5)
            elif self._user_is_pressing_skip_button(mouse_pos):
                self.current_player_move = AGENT
                self.show_skip_button = False
                self.can_get_new_card = True
                self.can_through_only_by_rank = False

    def _check_if_game_is_over(self):
        if len(self.agent_cards) == 0 or len(self.user_cards) == 0:
            self._draw_game_over(self.current_player_move)
            self.game_is_over = True

    def _render_skip_button(self):
        font = pg.font.SysFont('liberationmono', 60)

        skip_text = font.render('SKIP', True, Color.LIGHT_RED, Color.WHITE)
        pos_skip_text = skip_text.get_rect(center=(self.skip_button_pos.x, self.skip_button_pos.y))

        self.screen.blit(skip_text, pos_skip_text)
        pg.display.update()

    def _user_has_chosen_deck(self, mouse_pos):
        width, height = CARD_SIZE
        x, y = mouse_pos.x, mouse_pos.y

        fits_y = self.deck_position.y - height // 2 < y < self.deck_position.y + height // 2
        fits_x = self.deck_position.x - width // 2 < x < self.deck_position.x + width // 2

        return fits_y and fits_x

    def _update_animation(self):
        for move in self.sprite_moves:
            move.update()

            if move.is_completed():
                self.sprite_moves.remove(move)

    def _initialize_board(self):
        self.deck_cards = self._create_all_cards()

        self.agent_cards = set(sample(self.deck_cards, 5))
        self.deck_cards.difference_update(self.agent_cards)
        agent_cards_coords = [Point(100 + i * 90, 150) for i in range(len(self.agent_cards))]
        self.agent_cards_sprites.add([self.create_card(agent_cards_coords[i], Suit.back_side, Rank.back_side).sprite for i in range(len(self.agent_cards))])

        self.user_cards = set(sample(self.deck_cards, 4))
        self.deck_cards.difference_update(self.user_cards)
        self.user_cards_sprites.add([c.sprite for c in self.user_cards])

        self.card_in_action = self._get_random_card_from_deck()
        self.card_in_action_sprite_group.add(self.card_in_action.sprite)

        self.sprite_moves.append(SpriteMove([self.card_in_action.sprite], [self.table_center]))

        self.sprite_moves.append(SpriteMove(list(self.agent_cards_sprites), agent_cards_coords))

        user_cards_coords = [Point(100 + (i * 1.35) * 90, 750) for i in range(len(self.user_cards))]
        self.sprite_moves.append(SpriteMove(list(self.user_cards_sprites), user_cards_coords))

        self._check_the_effect()

    def _get_random_card_from_deck(self):
        random_card = choice(list(self.deck_cards))
        self.deck_cards.difference_update({random_card})

        if len(self.deck_cards) == 0:
            self._reshuffle_the_deck()

        return random_card

    def _create_all_cards(self):
        suits = [Suit.clubs, Suit.spades, Suit.diamonds, Suit.hearts]
        ranks = [Rank.six, Rank.seven, Rank.eight, Rank.nine, Rank.ten, Rank.jack, Rank.queen, Rank.king, Rank.ace]

        list_of_cards = {self.create_card(Point(*self.deck_position), suit, rank) for suit in suits for rank in ranks}

        return list_of_cards

    def can_make_move(self, chosen_card: Card):
        return self.card_in_action is None \
               or ((self.card_in_action.suit == chosen_card.suit or chosen_card.rank == Rank.jack) and not self.can_through_only_by_rank) \
               or self.card_in_action.rank == chosen_card.rank \

    def _user_is_pressing_skip_button(self, mouse_pos):
        fits_x = self.skip_button_pos.x - 50 < mouse_pos.x < self.skip_button_pos.x + 50
        fits_y = self.skip_button_pos.y - 50 < mouse_pos.y < self.skip_button_pos.y + 50

        return self.show_skip_button and fits_x and fits_y

    def _make_a_move(self, card: Card):
        self.deactivated_cards.add(self.card_in_action)

        if self.current_player_move == USER:
            self.user_cards.difference_update({card})
            self.user_cards_sprites.remove(card.sprite)

            user_cards_coords = [Point(100 + (i * 1.35) * 90, 750) for i in range(len(self.user_cards))]
            self.sprite_moves.append(SpriteMove(list(self.user_cards_sprites), user_cards_coords))
            self.sprite_moves.append(SpriteMove([card.sprite], [self.table_center]))
        else:
            self.agent_cards.difference_update({card})
            self.agent_cards_sprites = pg.sprite.Group([self.create_card(Point(100 + i * 90, 150), Suit.back_side, Rank.back_side).sprite for i in range(len(self.agent_cards))])
            card.sprite.pos = (100, 150)
            self.sprite_moves.append(SpriteMove([card.sprite], [self.table_center]))

        self.card_in_action = card
        self.card_in_action_sprite_group = pg.sprite.Group([card.sprite])

        self._check_the_effect()

    def _draw_game_over(self, winner):
        font = pg.font.SysFont('liberationmono', 60)
        game_over_text = font.render('GAME OVER', True, Color.LIGHT_RED, Color.WHITE)

        s_w, s_h = SCREEN_SIZE
        pos_game_over = game_over_text.get_rect(center=(s_w//2, s_h//2))

        winning_string = 'User is a winner' if winner == USER else 'Agent is a winner'
        winning_text = font.render(winning_string, True, Color.LIGHT_RED, Color.WHITE)
        pos_winner_text = winning_text.get_rect(center=(s_w//2, s_h//2 + 100))

        self.screen.blit(game_over_text, pos_game_over)
        self.screen.blit(winning_text, pos_winner_text)
        pg.display.update()

    @staticmethod
    def create_card(position: Point, suit, rank):
        return Card(suit=suit, rank=rank, pos_x=position.x, pos_y=position.y)

    def _check_the_effect(self):
        self.can_get_new_card = False
        self.show_skip_button = True
        self.can_through_only_by_rank = True
        self.six_in_action = False

        if self.card_in_action.rank == Rank.ace:
            self._opponent_skips_move()
        elif self.card_in_action.rank == Rank.eight:
            target_player = USER if self.current_player_move == AGENT else AGENT

            self._player_gets_a_card(target_player)
        elif self.card_in_action.rank == Rank.seven:
            target_player = USER if self.current_player_move == AGENT else AGENT

            self._player_gets_a_card(target_player)
            self._player_gets_a_card(target_player)

            self._opponent_skips_move()
        elif self.card_in_action.suit == Suit.spades and self.card_in_action.rank == Rank.queen:
            target_player = USER if self.current_player_move == AGENT else AGENT

            self._player_gets_a_card(target_player)
            self._player_gets_a_card(target_player)
            self._player_gets_a_card(target_player)
            self._player_gets_a_card(target_player)
            self._player_gets_a_card(target_player)

            self._opponent_skips_move()
        elif self.card_in_action.rank == Rank.six:
            self.six_in_action = True
            self.can_get_new_card = True
            self.show_skip_button = False
            self.can_through_only_by_rank = False

    def _player_gets_a_card(self, player):
        random_card = self._get_random_card_from_deck()

        if player == USER:
            self.user_cards.add(random_card)
            self.user_cards_sprites.add(random_card.sprite)

            destination_pos = Point(100 + ((len(self.user_cards) - 1) * 1.35) * 90, 750)
            self.sprite_moves.append(SpriteMove([random_card.sprite], [destination_pos]))
        else:
            self.agent_cards.add(random_card)
            card_sprite = self.create_card(self.deck_position, Suit.back_side, Rank.back_side).sprite
            self.agent_cards_sprites.add(card_sprite)

            destination_pos = Point(100 + (len(self.agent_cards) - 1) * 90, 150)
            self.sprite_moves.append(SpriteMove([card_sprite], [destination_pos]))

        if len(self.deck_cards) == 0:
            self._reshuffle_the_deck()

    def _opponent_skips_move(self):
        self.show_skip_button = False
        self.can_get_new_card = True
        self.can_through_only_by_rank = False

    def _reshuffle_the_deck(self):
        self.deck_cards = self.deactivated_cards
        self.deactivated_cards = set()

        backward_card_sprite = self.create_card(self.table_center, Suit.back_side, Rank.back_side).sprite
        self.sprite_moves.append(SpriteMove([backward_card_sprite], [self.deck_position]))

    def _ai_decide_which_move_to_make(self):
        ai_has_any_moves = len(self._ai_get_all_possible_moves())

        if self.can_get_new_card and not ai_has_any_moves:
            self._player_gets_a_card(AGENT)
            self.can_get_new_card = False
            self._ai_decide_which_move_to_make()
        elif not ai_has_any_moves:
            self._ai_finishes_his_move()
        else:
            self.can_get_new_card = False

            possible_moves = self._ai_get_all_possible_moves()
            best_card_to_move = max(possible_moves, key=self._ai_value_the_move)

            self._make_a_move(best_card_to_move)

    def _ai_get_all_possible_moves(self):
        moves = []
        for card in self.agent_cards:
            if self.can_make_move(card):
                if card.rank != Rank.six or self._ai_can_cover_six(card.suit):
                    moves.append(card)

        return moves

    def _ai_value_the_move(self, move_card: Card):
        if len(self.user_cards) == 1:
            return self._ai_value_the_move_in_danger_situation(move_card)

        suit, rank = move_card.suit, move_card.rank
        move_points = CARDS_POINTS_BY_RANK[rank]

        if rank == Rank.queen and suit == Suit.spades:
            move_points += 150

        move_points += (self._ai_count_cards_with_specific_rank(rank) - 1) * 60
        move_points += (self._ai_count_cards_with_specific_rank(rank) - 1) * CARDS_POINTS_BY_RANK[rank]

        if self._ai_count_cards_with_specific_suit(suit) == 1 and self._ai_count_cards_with_specific_rank(rank) == 1:
            move_points -= 70

        if move_card.rank == Rank.six:
            move_points += len(self._ai_find_max_rank_sequence(suit)) * 60

        return move_points

    def _ai_value_the_move_in_danger_situation(self, move_card: Card):
        suit, rank = move_card.suit, move_card.rank
        move_points = CARDS_POINTS_BY_RANK[rank]

        if rank == Rank.seven:
            move_points += 250 * self._ai_count_cards_with_specific_rank(Rank.seven)

        if rank == Rank.eight:
            move_points += 120 * self._ai_count_cards_with_specific_rank(Rank.eight)

        if rank == Rank.queen and suit == Suit.spades:
            move_points += 350

        if self._ai_count_cards_with_specific_suit(suit) == 1 and self._ai_count_cards_with_specific_rank(rank) == 1:
            move_points -= 70

        return move_points

    def _ai_count_cards_with_specific_rank(self, rank):
        result = 0
        for card in self.agent_cards:
            if card.rank == rank:
                result += 1

        return result

    def _ai_count_cards_with_specific_suit(self, suit):
        result = 0
        for card in self.agent_cards:
            if card.suit == suit:
                result += 1

        return result

    def _ai_finishes_his_move(self):
        self.can_get_new_card = True
        self.show_skip_button = False
        self.can_through_only_by_rank = False
        self.current_player_move = USER

    def _ai_through_all_possible_cards(self):
        possible_thoughts = []

        if self.card_in_action.rank == Rank.six:
            best_sequence = self._ai_find_best_sequence_to_cover_six(self.card_in_action.suit)
            self._make_a_move(best_sequence[0])
        else:
            for card in self.agent_cards:
                if self.card_in_action.rank == card.rank:
                    possible_thoughts.append(card)

            if possible_thoughts:
                self._make_a_move(max(possible_thoughts, key=self._ai_value_the_move))
            else:
                self._ai_finishes_his_move()

    def _ai_can_cover_six(self, six_suit, check_another_sixs=True):
        if self._ai_count_cards_with_specific_suit(six_suit) > 1:
            return True

        if self._ai_count_cards_with_specific_rank(Rank.six) > 1 and check_another_sixs:
            another_six = []
            for card in self.agent_cards:
                if card.rank == Rank.six and card.suit != six_suit:
                    another_six.append(card)

            return any([self._ai_can_cover_six(another_six.suit, check_another_sixs=False) for another_six in another_six])

    def _ai_find_best_sequence_to_cover_six(self, six_suit):
        max_sequence = self._ai_find_max_rank_sequence(six_suit)

        for card in self.agent_cards:
            if card.rank == Rank.six and card.suit != six_suit:
                new_best_sequence = self._ai_find_max_rank_sequence(card.suit)
                if len(new_best_sequence) + 1 > len(max_sequence):
                    max_sequence = [card]
                    max_sequence.extend(new_best_sequence)

        return max_sequence

    def _ai_find_max_rank_sequence(self, suit):
        max_sequence = []

        for card in self.agent_cards:
            if card.suit == suit and card.rank != Rank.six:
                if self._ai_count_cards_with_specific_rank(card.rank) > len(max_sequence):
                    max_sequence = [card]

                    for another_card in self.agent_cards:
                        if another_card.rank == card.rank and another_card.suit != card.suit:
                            max_sequence.append(another_card)

        return max_sequence
