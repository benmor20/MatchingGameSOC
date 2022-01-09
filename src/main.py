# import pygame
# from pygame import locals
from empiricaldist import Pmf
from matplotlib import pyplot as plt
import numpy as np

from src.model import MatchingModel
# from src.view import MatchingView
from src.controller import RandomController
from src.utils import *


def main():
    model = MatchingModel(10)
    model.setup()
    controller = RandomController(model)
    # view = MatchingView(model)
    # view.setup()
    # view.display_game()

    num_loops = 500000
    for i in range(num_loops):
        # for _ in pygame.event.get(locals.QUIT):
        #     return
        # view.display_game()
        if i % (num_loops // 100) == 0:
            print(100 * i // num_loops)
        controller.update()
        model.step()

    matches = np.array(model.num_matches)
    steps = np.array(model.num_steps)
    matches = matches[matches > 0]
    steps = steps[steps > 0]
    pmfMatch = Pmf.from_seq(matches)
    pmfStep = Pmf.from_seq(steps)

    plt.subplot(1, 2, 1)
    pmfMatch.plot(label='Matches')
    decorate(xlabel='Number of Matches', ylabel='PMF')

    plt.subplot(1, 2, 2)
    pmfStep.plot(label='Steps')
    decorate(xlabel='Number of Steps', ylabel='PMF')

    plt.show()


if __name__ == '__main__':
    main()