import logging

import numpy as np
from progress.bar import Bar

_logger = logging.getLogger(__name__)


def pick_random(array):
    return array[np.random.randint(array.shape[0], size=1), :][0]


def optimize(
    first_generation_generator,
    selection,
    crossover,
    mutation,
    fitness,
    max_generations,
    mutation_probability=0.2,
):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    population = np.array(first_generation_generator)
    population_len = len(population)
    _logger.debug("initial_population: %s", population)

    scores = list(map(fitness, population))
    _logger.debug("scores: %s", list(scores))
    _logger.debug("best score: %s", max(scores))

    bar = Bar("Processing", max=100)

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
        _logger.debug(
            "Generation: %s S: %s fitness: %s ",
            generation,
            the_best_match,
            fitness(the_best_match),
        )

        generation += 1
        bar.next()
        if generation >= max_generations:
            bar.finish()
            return the_best_match, fitness(the_best_match)
