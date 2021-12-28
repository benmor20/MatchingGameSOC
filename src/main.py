import pygame
from pygame import locals

import src.utils
from src import constants
from src.model import MatchingModel
from src.view import MatchingView
from src.controller import MatchingController


def main():
    model = MatchingModel(10)
    model.setup()
    controller = MatchingController(model)
    view = MatchingView(model)
    view.setup()
    view.display_game()

    clock = pygame.time.Clock()
    num_loops = 0

    while True:
        for _ in pygame.event.get(locals.QUIT):
            return
        if num_loops == 0 * constants.FPS:
            controller.update()
        view.display_game()
        # controller.update()
        clock.tick(constants.FPS)
        num_loops += 1


if __name__ == '__main__':
    main()