from typing import Callable, Optional

import pygame

OnFlipComplete = Callable[["Card"], None]


class Card:
    """A single memory-game card.

    Each card shows a graphic plus a Polish and Japanese word on its face,
    and a plain back while hidden. Two cards with the same `pair_id` are
    a match.
    """

    WIDTH: int = 100
    HEIGHT: int = 140
    BACK_COLOR: str = "steelblue"
    FACE_COLOR: str = "white"
    FLIP_DURATION: float = 0.25  # seconds, one half of the flip (hidden->edge or edge->shown)

    FONT_NAME: Optional[str] = None  # default pygame font; swap for a path that has JP glyphs
    FONT_SIZE: int = 16

    def __init__(
        self,
        pair_id: int,
        polish_text: str,
        japanese_text: str,
        image: Optional[pygame.Surface],
        pos: tuple[int, int],
    ) -> None:
        self.pair_id: int = pair_id
        self.polish_text: str = polish_text
        self.japanese_text: str = japanese_text
        self.image: Optional[pygame.Surface] = image

        self.rect: pygame.Rect = pygame.Rect(pos, (self.WIDTH, self.HEIGHT))

        self.is_hidden: bool = True
        self.is_matched: bool = False

        # animation state
        self._animating: bool = False
        self._anim_timer: float = 0.0
        self._pending_hidden_state: Optional[bool] = None  # target is_hidden once anim completes
        self._on_flip_complete: Optional[OnFlipComplete] = None

        self._font: pygame.font.Font = pygame.font.Font(self.FONT_NAME, self.FONT_SIZE)

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
        total_duration = self.FLIP_DURATION * 2

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
        half = self.FLIP_DURATION
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
            content, (max(1, int(self.WIDTH * scale_x)), self.HEIGHT)
        )
        blit_rect = scaled.get_rect(center=self.rect.center)
        surface.blit(scaled, blit_rect)

    def _render_back(self) -> pygame.Surface:
        surf = pygame.Surface((self.WIDTH, self.HEIGHT))
        surf.fill(self.BACK_COLOR)
        pygame.draw.rect(surf, "black", surf.get_rect(), width=2)
        return surf

    def _render_face(self) -> pygame.Surface:
        surf = pygame.Surface((self.WIDTH, self.HEIGHT))
        surf.fill(self.FACE_COLOR)
        pygame.draw.rect(surf, "black", surf.get_rect(), width=2)

        if self.image:
            img_rect = self.image.get_rect(midtop=(self.WIDTH // 2, 6))
            surf.blit(self.image, img_rect)

        pl_surf = self._font.render(self.polish_text, True, "black")
        jp_surf = self._font.render(self.japanese_text, True, "black")
        surf.blit(pl_surf, pl_surf.get_rect(centerx=self.WIDTH // 2, bottom=self.HEIGHT - 24))
        surf.blit(jp_surf, jp_surf.get_rect(centerx=self.WIDTH // 2, bottom=self.HEIGHT - 6))

        return surf
