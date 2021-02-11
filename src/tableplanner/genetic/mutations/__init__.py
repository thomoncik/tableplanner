import numpy as np


def swap_mutation(chromosome):
    idx = range(len(chromosome))
    i1, i2 = np.random.choice(idx, 2, replace=False)

    result = chromosome.copy()
    result[i1], result[i2] = result[i2], result[i1]

    return result
