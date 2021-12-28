from abc import ABC, abstractmethod
from typing import *

from src.model import MatchingModel
from src import constants


class Controller(ABC):
    def __init__(self, model: MatchingModel):
        self._model = model

    @abstractmethod
    def update(self):
        pass
