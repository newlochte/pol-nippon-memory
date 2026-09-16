import sys
from pathlib import Path

# ----------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------
# When frozen by PyInstaller, bundled data lives under sys._MEIPASS instead
# of next to this file.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)  # type: ignore[attr-defined]
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
DATA_DIR = BASE_DIR / "data"

# Latin font: covers Polish diacritics (ą ć ę ł ń ó ś ź ż) and romaji
# macrons (ā ī ū ē ō) — both are Latin Extended-A/B, so one font handles both.
LATIN_FONT_PATH = FONTS_DIR / "NotoSans-Regular.ttf"

# CJK font: needed for Japanese kanji/kana glyphs, which the Latin font
# does not contain. Drop a Japanese-capable .ttf/.otf/.ttc here.
JAPANESE_FONT_PATH = FONTS_DIR / "NotoSansJP[wght].ttf"

# ----------------------------------------------------------------------
# window / loop
# ----------------------------------------------------------------------
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
BACKGROUND_COLOR: str = "white"
WINDOW_TITLE: str = "Memory Game"

# ----------------------------------------------------------------------
# card appearance
# ----------------------------------------------------------------------
CARD_WIDTH: int = 140
CARD_HEIGHT: int = 100
CARD_BACK_COLOR: str = "steelblue"
CARD_FACE_COLOR: str = "white"
CARD_FLIP_DURATION: float = 0.25  # seconds, for the full flip animation
MISMATCH_FLIP_BACK_DELAY: float = 0.3  # seconds to pause on a non-matching pair before flipping back

# Font sizes are derived from card height (see Card._font_size_for) rather
# than fixed, so they stay proportional once card size becomes dynamic.
# At the current CARD_HEIGHT these reproduce the old fixed sizes (20/24).
LATIN_FONT_HEIGHT_RATIO: float = 0.20
JAPANESE_FONT_HEIGHT_RATIO: float = 0.24
MIN_FONT_SIZE: int = 8
MAX_FONT_SIZE: int = 48

# ----------------------------------------------------------------------
# board layout
# ----------------------------------------------------------------------
BOARD_MARGIN_X: int = 20
BOARD_MARGIN_Y: int = 20
BOARD_GAP: int = 10
