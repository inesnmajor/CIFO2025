from library.classes import FootballSolution
from library.crossover import crossover_teamwise_mix_and_repair,crossover_position_based, crossover_blockwise_teams_explained, crossover_position_based_explained
from library.mutation import mutate_swap_between_teams  # escolhe a tua mutação
from library.selection import tournament_selection
from library.crossover2child import crossover_position_based_explained_two_offspring, crossover_position_based_two_offspring, crossover_blockwise_teams_explained_two_offspring,crossover_blockwise_teams_two_offspring
import random
import numpy as np

# # Configurações
# POP_SIZE = 20
# N_GENERATIONS = 1
# ELITE_SIZE = 1
# MUTATION_RATE = 0.2

# # Inicialização da população
# population = [FootballSolution() for _ in range(POP_SIZE)]

# # Evolução
# for gen in range(N_GENERATIONS):
#     new_population = []

#     # Elitismo: manter os melhores
#     population.sort(key=lambda sol: sol.fitness(), reverse=True)
#     new_population.extend(population[:ELITE_SIZE])

#     # Gerar o resto da nova população
#     while len(new_population) < POP_SIZE:
#         # Seleção
#         parent1 = tournament_selection(population, k=3)
#         parent2 = tournament_selection(population, k=3)

#         # Crossover - GERA DOIS FILHOS
#         #child1, child2 = crossover_blockwise_teams_two_offspring(parent1, parent2)
#         child1= crossover_blockwise_teams_explained(parent1,parent2)
#         # Mutação no filho 1
#         if random.random() < MUTATION_RATE:
#             child1 = mutate_swap_between_teams(None, child1)

#         # Mutação no filho 2
#         # if random.random() < MUTATION_RATE:
#         #     child2 = mutate_swap_between_teams(None, child2)

#         # Adiciona os filhos se houver espaço
#         if len(new_population) < POP_SIZE:
#             new_population.append(child1)
#         # if len(new_population) < POP_SIZE:
#         #     new_population.append(child2)

#     population = new_population
#     best_fitness = max(ind.fitness() for ind in population)
#     print(f"\nGeneration {gen + 1} | Best fitness: {best_fitness:.4f}")

# # Melhor solução final
# best = max(population, key=lambda sol: sol.fitness())
# print("\n===== Best League Configuration =====")
# print(best)







#------------------------------------------------
#------------------------------------------------
#                   Rodrigo
#------------------------------------------------
#------------------------------------------------


from library.constraints import *
from library.crossover import *

#crossover_by_team_with_repair
#crossover_teamwise_mix_and_repair

# # Configurações
POP_SIZE = 19
N_GENERATIONS = 3
ELITE_SIZE = 1
MUTATION_RATE = 0.2

# Inicialização da população
population = [FootballSolution() for _ in range(POP_SIZE)]

# # Evolução
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
        child = crossover_blockwise_teams_explained(parent1, parent2)
        print(f"\n[DEBUG] Geração {gen+1} | Filho após crossover:")
        check_no_duplicates(child)
        check_team_size(child)
        # check_budget(child)
        check_team_structure(child)

        # Mutação
        if random.random() < MUTATION_RATE:
            child = mutate_swap_between_teams(None, child)
            print(f"\n[DEBUG] Geração {gen+1} | Filho após mutação:")
            check_no_duplicates(child)
            check_team_size(child)
            # check_budget(child)
            check_team_structure(child)

        new_population.append(child)

    check_no_duplicates(child)
    check_team_size(child)
    # check_budget(child)
    check_team_structure(child)
    population = new_population
    best_fitness = max(ind.fitness() for ind in population)
    print(f"Generation {gen+1} | Best fitness: {best_fitness:.4f}")

# Melhor solução final
best = max(population, key=lambda sol: sol.fitness())
print("\n===== Best League Configuration =====")
print(best)
