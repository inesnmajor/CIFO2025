import random
def tournament_selection(self, k=3):
        return max(random.sample(self.population, k), key=lambda s: s.fitness()).deepcopy()

def fitness_proportionate_selection(self):
    fitness_values = [ind.fitness() for ind in self.population]
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(self.population).deepcopy()
    rand = random.uniform(0, total_fitness)
    cumulative = 0
    for ind, fit in zip(self.population, fitness_values):
        cumulative += fit
        if rand <= cumulative:
            return ind.deepcopy()

def select_parent(self):
    return self.tournament_selection() if self.selection_method == "tournament" else self.fitness_proportionate_selection()
