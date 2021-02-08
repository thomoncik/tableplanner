def elite_selection(population, fitness):
    max_selected = max(2, int((len(population) + 9) / 10))
    sorted_by_fitness = sorted(population, key=fitness, reverse=True)

    return sorted_by_fitness[:max_selected]
