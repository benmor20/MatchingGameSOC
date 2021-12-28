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


def in_range(index, shape):
    for i, s in zip(index, shape):
        if i < 0 or i >= s:
            return False
    return True
