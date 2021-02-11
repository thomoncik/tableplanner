"""
Tests for `tableplanner.genetic.crossovers`
"""

import tableplanner.genetic.crossovers as crossovers


def test_order_crossover_does_not_duplicate_elements():
    """Order crossover should not remove/add elements; only create a permutation"""
    parent_1 = [3, 4, 8, 2, 7, 1, 6, 5]
    parent_2 = [4, 2, 5, 1, 6, 8, 3, 7]
    assert sorted(crossovers.order_crossover(parent_1, parent_2)) == sorted(parent_1)
    assert sorted(crossovers.order_crossover(parent_1, parent_2)) == sorted(parent_2)
