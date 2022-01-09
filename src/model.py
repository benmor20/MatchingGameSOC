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
        shape = n, n if m is None else m
        self.grid = np.zeros(shape, dtype=int)
        self.num_matches_by_step = []
        self.duration = []
        self.num_matches_by_loop = []

    @property
    def num_colors(self):
        return len(self.colors)

    def setup(self):
        self.grid = np.random.randint(0, self.num_colors, self.grid.shape)
        self.loop_until_done()

    def _get_match_array(self, kernel):
        corr = correlate2d(self.grid, kernel, mode='same')
        c10 = self.num_colors
        c100 = c10 * self.num_colors
        c1000 = c100 * self.num_colors
        c111 = c100 + c10 + 1
        right3 = (corr % c1000) % c111 == 0
        left3 = (corr // c100) % c111 == 0
        mid3 = ((corr // c10) % c1000) % c111 == 0
        return right3 | left3 | mid3

    def get_matches(self):
        horz_kernel = np.array([self.num_colors ** i for i in range(5)]).reshape(1, -1)
        vert_kernel = horz_kernel.copy().T
        return self._get_match_array(horz_kernel) | self._get_match_array(vert_kernel)

    def step(self):
        # Find matches
        matches = self.get_matches()
        total_matches = np.sum(matches)
        if total_matches == 0:
            return matches

        # Empty matches
        self.grid[matches] = -2

        # Drop remaining
        for j in range(self.grid.shape[1]):
            for i in range(self.grid.shape[0] - 1, -1, -1):
                while self.grid[i][j] == -2:
                    self.grid[1:i+1, j] = self.grid[:i, j]
                    self.grid[0, j] = -1

        # Fill empty
        empties = self.grid == -1
        self.grid[empties] = np.random.randint(0, self.num_colors, self.grid.shape)[empties]

        return matches

    def loop_until_done(self, func=None):
        self.num_matches_by_loop.append(0)
        self.duration.append(0)
        while True:
            matches = self.step()
            total_matches = np.sum(matches)
            if total_matches == 0:
                return
            self.num_matches_by_loop[-1] += total_matches
            self.num_matches_by_step.append(total_matches)
            self.duration[-1] += 1
            if func is not None:
                func(matches)
