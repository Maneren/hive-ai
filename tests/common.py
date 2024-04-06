import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))

board_size = 13
small_figures = {
    "q": 1,
    "a": 2,
    "b": 2,
    "s": 2,
    "g": 2,
}
big_figures = {figure.upper(): val for figure, val in small_figures.items()}
