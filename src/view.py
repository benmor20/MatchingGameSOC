import pygame
from pygame import locals
from typing import *
from abc import ABC, abstractmethod
import itertools

from src.model import MatchingModel
from src import constants
from src import utils


class View(ABC):
    def __init__(self, model: MatchingModel):
        self._model = model

    def setup(self):
        return

    @abstractmethod
    def display_game(self):
        pass

    def teardown(self):
        return


class PygameView(View, ABC):
    def __init__(self, model: MatchingModel,
                 screen_size: Union[Tuple[int, int], pygame.Surface] = constants.SCREEN_SIZE,
                 default_background: Tuple[int, int, int] = constants.BACKGROUND_COLOR):
        super().__init__(model)
        if not pygame.get_init():
            pygame.init()
        self._screen = screen_size if isinstance(screen_size, pygame.Surface) else pygame.display.set_mode(screen_size)
        self.background = default_background

    @property
    def screen(self):
        return self._screen

    def display_game(self):
        if len(pygame.event.get(eventtype=locals.QUIT)) > 0:
            self._model.running = False
        self._screen.fill(self.background)
        self._draw()
        pygame.display.flip()

    @abstractmethod
    def _draw(self):
        pass


class MatchingView(PygameView):
    def __init__(self, model: MatchingModel, square_size: Tuple[int, int] = (30, 30), gap_size: int = 5,
                 board_midtop: Tuple[int, int] = (-1, 100), board_color: Tuple[int, int, int] = constants.BOARD_COLOR,
                 screen_size: Union[Tuple[int, int], pygame.Surface] = constants.SCREEN_SIZE,
                 default_background: Tuple[int, int, int] = constants.BACKGROUND_COLOR):
        super().__init__(model, screen_size, default_background)
        self._gap_size = gap_size
        self._square_size = square_size
        board_size = self._board_pos_from_grid_pos(self._model.grid.shape)
        self._board = pygame.Surface(board_size)
        board_mid = constants.SCREEN_SIZE[0] // 2 if board_midtop[0] == -1 else board_midtop[0]
        self._board_rect = self._board.get_rect(midtop=(board_mid, board_midtop[1]))
        self.board_color = board_color

    def _board_pos_from_grid_pos(self, grid_pos):
        return utils.combine_tuples([self._square_size, grid_pos], lambda l: (l[0] + self._gap_size) * l[1] + self._gap_size)

    def _draw(self):
        self._board.fill(self.board_color)
        for i, j in utils.indexes(self._model.grid.shape):
            color = self._model.grid[i, j]
            color = self._model.colors[color]
            if color is None:
                color = self.board_color
            coords = self._board_pos_from_grid_pos((i, j))
            pygame.draw.rect(self._board, color, pygame.Rect(*coords, *self._square_size))
        self._screen.blit(self._board, self._board_rect)
