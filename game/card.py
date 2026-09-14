from typing import Callable, ClassVar, Optional

import pygame

from game.constants import (
    CARD_BACK_COLOR,
    CARD_FACE_COLOR,
    CARD_FLIP_DURATION,
    CARD_HEIGHT,
    CARD_WIDTH,
    JAPANESE_FONT_PATH,
    JAPANESE_FONT_SIZE,
    LATIN_FONT_PATH,
    LATIN_FONT_SIZE,
)

OnFlipComplete = Callable[["Card"], None]

# (japanese, romaji, english, polish)
WordTuple = tuple[str, str, str, str]


class Card:
    """A single memory-game card.

    Each card shows a graphic plus a word's Japanese, romaji, English, and
    Polish forms on its face, and a plain back while hidden. Two cards with
    the same `pair_id` are a match.
    """

    # Fonts are expensive to load and identical across every card, so they're
    # loaded once and shared at the class level rather than per instance.
    _latin_font: ClassVar[Optional[pygame.font.Font]] = None
    _japanese_font: ClassVar[Optional[pygame.font.Font]] = None

    def __init__(
        self,
        pair_id: int,
        word: WordTuple,
        image: Optional[pygame.Surface],
        pos: tuple[int, int],
    ) -> None:
        self.pair_id: int = pair_id
        self.japanese, self.romaji, self.english, self.polish = word
        self.image: Optional[pygame.Surface] = image

        self.rect: pygame.Rect = pygame.Rect(pos, (CARD_WIDTH, CARD_HEIGHT))

        self.is_hidden: bool = True
        self.is_matched: bool = False

        # animation state
        self._animating: bool = False
        self._anim_timer: float = 0.0
        self._pending_hidden_state: Optional[bool] = None  # target is_hidden once anim completes
        self._on_flip_complete: Optional[OnFlipComplete] = None

        self._ensure_fonts_loaded()

    # ------------------------------------------------------------------
    # fonts
    # ------------------------------------------------------------------
    @classmethod
    def _ensure_fonts_loaded(cls) -> None:
        """Load the shared fonts once, on first Card construction."""
        if cls._latin_font is not None and cls._japanese_font is not None:
            return

        if not LATIN_FONT_PATH.exists():
            raise FileNotFoundError(
                f"Missing Latin font at {LATIN_FONT_PATH}. It covers Polish "
                "diacritics and romaji macrons."
            )
        if not JAPANESE_FONT_PATH.exists():
            raise FileNotFoundError(
                f"Missing Japanese font at {JAPANESE_FONT_PATH}. Download a "
                "Japanese-capable .ttf/.otf (e.g. Noto Sans JP) and place it "
                "there."
            )

        cls._latin_font = pygame.font.Font(str(LATIN_FONT_PATH), LATIN_FONT_SIZE)
        cls._japanese_font = pygame.font.Font(str(JAPANESE_FONT_PATH), JAPANESE_FONT_SIZE)

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------
    def flip(self, on_complete: Optional[OnFlipComplete] = None) -> Optional[int]:
        """Start flipping the card to its opposite state.

        Returns the card's pair_id immediately if it is *becoming* shown,
        or None if it is becoming hidden or already mid-animation.
        `on_complete` (optional) is called with this card once the
        animation finishes flipping.
        """
        if self._animating or self.is_matched:
            return None

        self._pending_hidden_state = not self.is_hidden
        self._animating = True
        self._anim_timer = 0.0
        self._on_flip_complete = on_complete

        return None if self._pending_hidden_state else self.pair_id

    def update(self, dt: float) -> None:
        """Advance the flip animation. Call once per frame from Game._update."""
        if not self._animating:
            return

        self._anim_timer += dt
        total_duration = CARD_FLIP_DURATION * 2

        if self._anim_timer >= total_duration:
            assert self._pending_hidden_state is not None
            self._animating = False
            self.is_hidden = self._pending_hidden_state
            self._pending_hidden_state = None
            if self._on_flip_complete:
                self._on_flip_complete(self)
                self._on_flip_complete = None

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the card, accounting for the in-progress flip animation."""
        if self._animating:
            self._draw_animated(surface)
            return

        content = self._render_back() if self.is_hidden else self._render_face()
        surface.blit(content, self.rect)

    def contains(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------
    def _draw_animated(self, surface: pygame.Surface) -> None:
        """Squash the card horizontally to 0 width then back out, swapping
        which face is shown at the halfway point."""
        half = CARD_FLIP_DURATION
        showing_hidden: bool
        if self._anim_timer < half:
            # shrinking: show current (pre-flip) side
            progress = self._anim_timer / half
            showing_hidden = self.is_hidden
        else:
            # growing: show the new (post-flip) side
            progress = 1 - (self._anim_timer - half) / half
            assert self._pending_hidden_state is not None
            showing_hidden = self._pending_hidden_state

        scale_x = max(abs(progress), 0.01)
        content = self._render_back() if showing_hidden else self._render_face()
        scaled = pygame.transform.scale(
            content, (max(1, int(CARD_WIDTH * scale_x)), CARD_HEIGHT)
        )
        blit_rect = scaled.get_rect(center=self.rect.center)
        surface.blit(scaled, blit_rect)

    def _render_back(self) -> pygame.Surface:
        surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        surf.fill(CARD_BACK_COLOR)
        pygame.draw.rect(surf, "black", surf.get_rect(), width=2)
        return surf

    def _render_face(self) -> pygame.Surface:
        assert self._latin_font is not None and self._japanese_font is not None

        surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        surf.fill(CARD_FACE_COLOR)
        pygame.draw.rect(surf, "black", surf.get_rect(), width=2)

        if self.image:
            img_rect = self.image.get_rect(midtop=(CARD_WIDTH // 2, 6))
            surf.blit(self.image, img_rect)

        # Japanese uses the CJK font; romaji/English/Polish share the Latin
        # font, which also covers Polish diacritics and romaji macrons.
        lines = [
            (self.japanese, self._japanese_font),
            (self.romaji, self._latin_font),
            (self.english, self._latin_font),
            (self.polish, self._latin_font),
        ]

        line_surfaces = [font.render(text, True, "black") for text, font in lines]
        bottom = CARD_HEIGHT - 6
        for line_surf in reversed(line_surfaces):
            surf.blit(line_surf, line_surf.get_rect(centerx=CARD_WIDTH // 2, bottom=bottom))
            bottom -= line_surf.get_height() + 2

        return surf
