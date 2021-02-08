import logging

import numpy as np

_logger = logging.getLogger(__name__)


def pick_random(array):
    return array[np.random.randint(array.shape[0], size=1), :][0]


def optimize(
    first_generation_generator,
    selection,
    crossover,
    mutation,
    fitness,
    stop_condition,
    mutation_probability=0.2,
):
    population = np.array(
        first_generation_generator
    )  # np.array([np.random.permutation(range(len(guest_names))) for _ in range(10)])
    population_len = len(population)
    _logger.debug("initial_population: {}", population)

    scores = list(map(fitness, population))
    _logger.debug("scores: {}", list(scores))
    _logger.debug("best score: {}", max(scores))

    generation = 0
    while True:
        selected = selection(population, fitness)
        new_population = selected.copy()
        while len(new_population) != population_len:
            child = crossover(pick_random(population), pick_random(population))
            if np.random.random() <= mutation_probability:
                child = mutation(child)
            new_population.append(child)

        population = np.array(new_population)
        the_best_match = max(population, key=fitness)
        print(
            "Generation: {} S: {} fitness: {}".format(
                generation, the_best_match, fitness(the_best_match)
            )
        )

        generation += 1
        if generation >= 100:  # stop condition
            return the_best_match, fitness(the_best_match)
