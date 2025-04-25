from library.classes import FootballSolution
from library.crossover import crossover_teamwise_mix_and_repair,crossover_by_team_with_repair
from library.mutation import mutate_swap_between_teams  # escolhe a tua mutação
from library.selection import tournament_selection
import random

# Configurações
POP_SIZE = 20
N_GENERATIONS = 30
ELITE_SIZE = 1
MUTATION_RATE = 0.2

# Inicialização da população
population = [FootballSolution() for _ in range(POP_SIZE)]

# Evolução
for gen in range(N_GENERATIONS):
    new_population = []

    # Elitismo: manter os melhores
    population.sort(key=lambda sol: sol.fitness(), reverse=True)
    new_population.extend(population[:ELITE_SIZE])

    # Gerar o resto da nova população
    while len(new_population) < POP_SIZE:
        # Seleção
        parent1 = tournament_selection(population, k=3)
        parent2 = tournament_selection(population, k=3)

        # Crossover
        child = crossover_by_team_with_repair(parent1, parent2)

        # Mutação
        if random.random() < MUTATION_RATE:
            child = mutate_swap_between_teams(None, child)

        new_population.append(child)

    population = new_population
    best_fitness = max(ind.fitness() for ind in population)
    print(f"Generation {gen+1} | Best fitness: {best_fitness:.4f}")

# Melhor solução final
best = max(population, key=lambda sol: sol.fitness())
print("\n===== Best League Configuration =====")
print(best)
