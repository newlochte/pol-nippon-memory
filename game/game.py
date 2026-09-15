import random
from typing import Optional

import math
from typing import Optional

import math
import pygame

from game.words import WordTuple, load_words
from game.card import Card
from game.config import (
    BACKGROUND_COLOR,
    BOARD_GAP,
    BOARD_MARGIN_X,
    BOARD_MARGIN_Y,
    CARD_HEIGHT,
    CARD_WIDTH,
    FPS,
    MISMATCH_FLIP_BACK_DELAY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINDOW_TITLE,
)


class Game:
    """Owns the main loop and top-level game state."""

    def __init__(self, pair_count: int) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = False

        # game state
        self.board_size = self._pair2colrow(pair_count)
        self.cards: list[Card] = []
        self.selected_cards: list[Card] = []  # currently flipped, unmatched cards
        self.matched_pairs: int = 0
        self.score: int = 0
        self._mismatch_timer: Optional[float] = None  # counts down while a non-matching pair is shown

        self._load_assets()
        self._setup_board()

    # ------------------------------------------------------------------
    # setup
    # ------------------------------------------------------------------
    @staticmethod
    def _pair2colrow(pair_count: int) -> tuple[int, int]:
        card_count = pair_count * 2
        rows = math.isqrt(card_count)

        while card_count % rows != 0:
            rows -= 1

        cols = card_count // rows
        return cols, rows
    

    def _load_assets(self) -> None:
        """Load images/sounds once up front."""
        pass

    def _setup_board(self) -> None:
        """Create and shuffle the cards, position them on a grid."""
        cols, rows = self.board_size
        pair_count = (cols * rows) // 2
        # (japanese, romaji, english, polish)
        vocab: list[WordTuple] = random.sample(load_words(), k=pair_count)
        
        pairs: list[tuple[int, WordTuple]] = []
        for pair_id, word in enumerate(vocab):
            pairs.append((pair_id, word))
            pairs.append((pair_id, word))
        random.shuffle(pairs)

        for index, (pair_id, word) in enumerate(pairs):
            col = index % cols
            row = index // cols
            x = BOARD_MARGIN_X + col * (CARD_WIDTH + BOARD_GAP)
            y = BOARD_MARGIN_Y + row * (CARD_HEIGHT + BOARD_GAP)
            self.cards.append(Card(pair_id, word, image=None, pos=(x, y)))

    # ------------------------------------------------------------------
    # main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # seconds since last frame
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

    def _handle_click(self, pos: tuple[int, int]) -> None:
        """Translate a click position into a card flip, if any."""
        if len(self.selected_cards) >= 2:
            return  # waiting for the current pair to resolve/flip back

        for card in self.cards:
            if card.contains(pos) and card.is_hidden and not card.is_matched:
                card.flip(on_complete=self._on_card_flipped)
                self.selected_cards.append(card)
                break

    def _on_card_flipped(self, card: Card) -> None:
        """Called by a Card once its flip animation finishes."""
        if len(self.selected_cards) < 2:
            return
        if card is not self.selected_cards[-1]:
            return  # only react once the second card's animation has landed

        first, second = self.selected_cards
        if first.pair_id == second.pair_id:
            first.is_matched = True
            second.is_matched = True
            self.matched_pairs += 1
            self.score += 1
            self.selected_cards = []
        else:
            self._mismatch_timer = MISMATCH_FLIP_BACK_DELAY

    def _update(self, dt: float) -> None:
        """Advance card animations, the mismatch pause, and check the win condition."""
        for card in self.cards:
            card.update(dt)

        if self._mismatch_timer is not None:
            self._mismatch_timer -= dt
            if self._mismatch_timer <= 0:
                self._mismatch_timer = None
                first, second = self.selected_cards
                first.flip(on_complete=lambda c: None)
                second.flip(on_complete=lambda c: None)
                self.selected_cards = []

        total_pairs = (self.board_size[0] * self.board_size[1]) // 2
        if self.matched_pairs == total_pairs:
            self.running = False  # TODO: show a win screen instead

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        for card in self.cards:
            card.draw(self.screen)

        pygame.display.flip()
