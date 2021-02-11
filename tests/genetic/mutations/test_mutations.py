"""
Tests for `tableplanner.genetic.mutations`
"""

import tableplanner.genetic.mutations as mutations


def test_swap_mutations_change_exactly_two_elements():
    """Swap mutation should change exactly two elements, other should remain the same"""
    chromosome = [3, 4, 8, 2, 7, 1, 6, 5]
    assert sorted(mutations.swap_mutation(chromosome)) == sorted(chromosome)
    assert (
        sum(
            1 for x, y in zip(chromosome, mutations.swap_mutation(chromosome)) if x != y
        )
        == 2
    )
