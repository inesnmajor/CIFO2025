import random
def tournament_selection(population, k=3):
    return max(random.sample(population, k), key=lambda s: s.fitness()).deepcopy()

def fitness_proportionate_selection(population):
    fitness_values = [ind.fitness() for ind in population]
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population).deepcopy()
    rand = random.uniform(0, total_fitness)
    cumulative = 0
    for ind, fit in zip(population, fitness_values):
        cumulative += fit
        if rand <= cumulative:
            return ind.deepcopy()
