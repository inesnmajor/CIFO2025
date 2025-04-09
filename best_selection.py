from library.selection import tournament_selection, fitness_proportionate_selection
from library.crossover import team_swap_crossover, team_two_point_crossover
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team

import random
import numpy as np

def run_ga_test(selection_func, crossover_func, mutation_func, generations=30, pop_size=20):
    population = [FootballSolution() for _ in range(pop_size)]

    best_fitness_progress = []

    for gen in range(generations):
        new_population = []
        for _ in range(pop_size // 2):
            p1 = selection_func(population)
            p2 = selection_func(population)

            c1, c2 = crossover_func(None, p1, p2)

            c1 = mutation_func(None, c1)
            c2 = mutation_func(None, c2)

            new_population.extend([c1, c2])

        population = new_population
        best_fitness = max(ind.fitness() for ind in population)
        best_fitness_progress.append(best_fitness)

    return best_fitness_progress, np.mean(best_fitness_progress[-5:])  # média das últimas 5 gerações

# Combinações possíveis
selection_methods = {
    "tournament": tournament_selection,
    "fitness_proportionate": fitness_proportionate_selection
}

crossover_methods = {
    "team_swap": team_swap_crossover,
    "team_two_point": team_two_point_crossover
}

mutation_methods = {
    "global_perm": mutate_global_position_permutation,
    "random_swap": mutate_random_position_swap,
    "between_teams": mutate_swap_between_teams
}

# Testar todas as combinações
results = []

for sel_name, sel_func in selection_methods.items():
    for cross_name, cross_func in crossover_methods.items():
        for mut_name, mut_func in mutation_methods.items():
            print(f"Testing {sel_name} | {cross_name} | {mut_name}")
            fitness_prog, final_avg = run_ga_test(sel_func, cross_func, mut_func)
            results.append({
                "selection": sel_name,
                "crossover": cross_name,
                "mutation": mut_name,
                "final_avg_fitness": final_avg
            })

# Mostrar resultados ordenados
results.sort(key=lambda x: x["final_avg_fitness"], reverse=True)

print("\nMelhores combinações (ordenadas por média da fitness final):\n")
print("{:<25} {:<20} {:<20} {:<10}".format("Selection", "Crossover", "Mutation", "Fitness"))

for res in results:
    print("{:<25} {:<20} {:<20} {:.4f}".format(
        res["selection"],
        res["crossover"],
        res["mutation"],
        res["final_avg_fitness"]
    ))
