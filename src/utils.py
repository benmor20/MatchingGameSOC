from typing import *
import itertools
from matplotlib import pyplot as plt


def combine_tuples(tuples: Iterable[Tuple], func: Callable[[Iterable], Any] = sum):
    return tuple(func(vals) for vals in zip(*tuples))


def subtract(vals: Iterable):
    res = 0
    for i, v in enumerate(vals):
        if i == 0:
            res = v
        else:
            res -= v
    return res


def indexes(shape):
    yield from itertools.product(*[range(s) for s in shape])


def in_range(index, shape):
    for i, s in zip(index, shape):
        if i < 0 or i >= s:
            return False
    return True


def decorate(**options):
    """From https://github.com/AllenDowney/ThinkComplexity2/raw/master/notebooks/utils.py

    Decorate the current axes.

    Call decorate with keyword arguments like

    decorate(title='Title',
             xlabel='x',
             ylabel='y')

    The keyword arguments can be any of the axis properties

    https://matplotlib.org/api/axes_api.html

    In addition, you can use `legend=False` to suppress the legend.

    And you can use `loc` to indicate the location of the legend
    (the default value is 'best')
    """
    loc = options.pop("loc", "best")
    if options.pop("legend", True):
        legend(loc=loc)

    plt.gca().set(**options)
    plt.tight_layout()


def legend(**options):
    """From https://github.com/AllenDowney/ThinkComplexity2/raw/master/notebooks/utils.py

    Draws a legend only if there is at least one labeled item.

    options are passed to plt.legend()
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html

    """
    underride(options, loc="best", frameon=False)

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, **options)


def underride(d, **options):
    """From https://github.com/AllenDowney/ThinkComplexity2/raw/master/notebooks/utils.py

    Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d
