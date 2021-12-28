from src import constants
import numpy as np
from scipy.signal import correlate2d
from typing import *


class MatchingModel:
    def __init__(self, n: int, m: Optional[int] = None, colors: Union[Iterable[Tuple[int, int, int]], int] = 4):
        if isinstance(colors, int):
            assert colors <= len(constants.COLORS)
            self.colors = constants.COLORS[:colors]
        else:
            self.colors = list(colors)
        self.colors = [None] + self.colors
        shape = n, n if m is None else m
        self.grid = np.zeros(shape, dtype=int)

    @property
    def num_colors(self):
        return len(self.colors)

    def setup(self):
        self.grid = np.random.randint(1, self.num_colors, self.grid.shape)
        # self.step()

    def _to_color_base(self, digits):
        return sum(d * self.num_colors ** i for i, d in enumerate(digits[::-1]))

    def _get_match_array(self, kernel):
        corr = correlate2d(self.grid, kernel, mode='same')
        c10 = self._to_color_base([1, 0])
        c100 = c10 * self.num_colors
        c1000 = c100 * self.num_colors
        c111 = c100 + c10 + 1
        right3 = (corr % c1000) % c111 == 0
        left3 = (corr // c100) % c111 == 0
        mid3 = ((corr // c10) % c1000) % c111 == 0
        return right3 | left3 | mid3

    def step(self):
        # Find matches
        horz_kernel = np.array([self.num_colors ** i for i in range(5)]).reshape(-1, 1)
        vert_kernel = horz_kernel.copy().T
        matches = self._get_match_array(horz_kernel) | self._get_match_array(vert_kernel)

        # Empty matches
        self.grid[matches] = 0

        # Drop remaining
        # Fill empty
        pass

    # 11111
    # 1111_
    # 111__
    # _1111
    # _111_
    # __111
