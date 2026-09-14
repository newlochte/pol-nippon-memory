import pygame


class Game:
    """Owns the main loop and top-level game state."""

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    FPS = 60
    BACKGROUND_COLOR = "white"

    def __init__(self, board_size: tuple[int, int]):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Memory Game")
        self.clock = pygame.time.Clock()
        self.running = False

        # game state
        self.cards = []          # will hold Card instances
        self.selected_cards = [] # currently flipped, unmatched cards
        self.matched_pairs = 0
        self.score = 0

        self._load_assets()
        self._setup_board()

    # ------------------------------------------------------------------
    # setup
    # ------------------------------------------------------------------
    def _load_assets(self):
        """Load images/sounds once up front."""
        pass

    def _setup_board(self):
        """Create and shuffle the cards, position them on a grid."""
        pass

    # ------------------------------------------------------------------
    # main loop
    # ------------------------------------------------------------------
    def run(self):
        self.running = True
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(self.FPS)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

    def _handle_click(self, pos):
        """Translate a click position into a card flip, if any."""
        pass

    def _update(self):
        """Check for matches, handle flip-back timing, win condition, etc."""
        pass

    def _draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)

        
        
        pygame.display.flip()
