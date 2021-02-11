"""
Tests for `tableplanner.genetic.selections`
"""

import tableplanner.genetic.selections as selections


def test_elite_selection_selects_at_least_two_elements():
    """
    Elite selection choose the two greatest elements with arrays sized 8
    """
    population = [3, 4, 8, 2, 7, 1, 6, 5]
    assert sorted(selections.elite_selection(population, lambda x: x)) == [7, 8]
