from typing import *
import itertools


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
