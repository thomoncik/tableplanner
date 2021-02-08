from itertools import cycle, islice

import numpy as np


def order_crossover(parent_1, parent_2):
    mark_1 = np.random.randint(0, len(parent_1) - 1)
    mark_2 = np.random.randint(mark_1 + 1, len(parent_1))

    offspring = [
        parent_1[i] if mark_1 <= i < mark_2 else None for i in range(0, len(parent_1))
    ]
    foo = islice(cycle(parent_2), mark_2, None)

    for i in range(mark_2, len(parent_1)):
        if offspring[i] is None:
            v = next(foo)
            while v in parent_1[mark_1:mark_2]:
                v = next(foo)
            offspring[i] = v

    for i in range(0, mark_1):
        if offspring[i] is None:
            v = next(foo)
            while v in parent_1[mark_1:mark_2]:
                v = next(foo)
            offspring[i] = v

    return offspring
