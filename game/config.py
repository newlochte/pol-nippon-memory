from pathlib import Path

# ----------------------------------------------------------------------
# paths
# ----------------------------------------------------------------------
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

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
CARD_FLIP_DURATION: float = 0.25  # seconds, one half of the flip (hidden->edge or edge->shown)

LATIN_FONT_SIZE: int = 14
JAPANESE_FONT_SIZE: int = 16

# ----------------------------------------------------------------------
# board layout
# ----------------------------------------------------------------------
BOARD_MARGIN_X: int = 20
BOARD_MARGIN_Y: int = 20
BOARD_GAP: int = 10
