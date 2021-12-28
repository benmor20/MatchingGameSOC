from abc import ABC, abstractmethod
import numpy as np
from typing import *

from src.model import MatchingModel
from src import constants
from src.utils import *


class Controller(ABC):
    def __init__(self, model: MatchingModel):
        self._model = model

    @abstractmethod
    def update(self):
        pass


class MatchingController(Controller):
    def update(self):
        index = tuple(np.random.randint(0, self._model.grid.shape))
        direcs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        direc = direcs[np.random.choice([d for d in range(4) if in_range(combine_tuples([index, direcs[d]]),
                                                                         self._model.grid.shape)])]
        swap = combine_tuples([index, direc])
        self._model.grid[index], self._model.grid[swap] = self._model.grid[swap], self._model.grid[index]
