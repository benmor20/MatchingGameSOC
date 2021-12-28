import pygame
from pygame import locals

import src.utils
from src import constants
from src.model import MatchingModel
from src.view import MatchingView


def main():
    model = MatchingModel(10)
    model.setup()
    view = MatchingView(model)
    view.setup()
    view.display_game()

    clock = pygame.time.Clock()
    num_loops = 0

    while True:
        for _ in pygame.event.get(locals.QUIT):
            return
        if num_loops == 2 * constants.FPS:
            print(model.grid)
            model.step()
            print(model.grid)
        view.display_game()
        # controller.update()
        clock.tick(constants.FPS)
        num_loops += 1


if __name__ == '__main__':
    main()