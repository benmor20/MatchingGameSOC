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
        self.num_matches = []
        self.num_steps = []

    @property
    def num_colors(self):
        return len(self.colors)

    def setup(self):
        self.grid = np.random.randint(1, self.num_colors, self.grid.shape)
        self.step()

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
        self.num_matches.append(0)
        self.num_steps.append(0)
        while True:
            # Find matches
            horz_kernel = np.array([self.num_colors ** i for i in range(5)]).reshape(-1, 1)
            vert_kernel = horz_kernel.copy().T
            matches = self._get_match_array(horz_kernel) | self._get_match_array(vert_kernel)
            total_matches = np.sum(matches)
            if total_matches == 0:
                return
            self.num_matches[-1] += total_matches
            self.num_steps[-1] += 1

            # Empty matches
            self.grid[matches] = -1

            # Drop remaining
            for j in range(self.grid.shape[1]):
                for i in range(self.grid.shape[0] - 1, -1, -1):
                    while self.grid[i][j] == -1:
                        self.grid[1:i+1, j] = self.grid[:i, j]
                        self.grid[0, j] = 0

            # Fill empty
            empties = self.grid == 0
            self.grid[empties] = np.random.randint(1, self.num_colors, self.grid.shape)[empties]
