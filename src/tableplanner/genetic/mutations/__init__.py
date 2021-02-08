import numpy as np


def swap_mutation(chromosome):
    idx = range(len(chromosome))
    i1, i2 = np.random.choice(idx, 2)
    chromosome[i1], chromosome[i2] = chromosome[i2], chromosome[i1]

    return chromosome
