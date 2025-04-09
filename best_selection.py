from library.selection import tournament_selection, fitness_proportionate_selection
from library.crossover import team_swap_crossover, team_two_point_crossover
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team

import random
import numpy as np

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

def run_ga_test(selection_func, crossover_func, mutation_func,
                generations=30, pop_size=20, elitism=True, n_runs=30):
    
    final_best_fitnesses = []

    for run in range(n_runs):
        population = [FootballSolution() for _ in range(pop_size)]
        
        for gen in range(generations):
            new_population = []

            if elitism:
                elite = max(population, key=lambda ind: ind.fitness()).deepcopy()

            for _ in range(pop_size // 2):
                p1 = selection_func(population)
                p2 = selection_func(population)

                c1, c2 = crossover_func(None, p1, p2)
                c1 = mutation_func(None, c1)
                c2 = mutation_func(None, c2)

                new_population.extend([c1, c2])

            if elitism:
                worst_idx = min(range(len(new_population)), key=lambda i: new_population[i].fitness())
                new_population[worst_idx] = elite

            population = new_population

        # 🔹 Guardar melhor fitness ao final da run
        final_best = max(ind.fitness() for ind in population)
        final_best_fitnesses.append(final_best)

    # 🔸 Retorna a mediana dos 30 melhores fitness finais
    return np.median(final_best_fitnesses), final_best_fitnesses



results = []

for elitism_flag in [True, False]:
    for sel_name, sel_func in selection_methods.items():
        for cross_name, cross_func in crossover_methods.items():
            for mut_name, mut_func in mutation_methods.items():
                name = f"{sel_name}|{cross_name}|{mut_name}|elitism={elitism_flag}"
                print(f"\nRunning {name} ...")

                median_final, all_finals = run_ga_test(
                    sel_func, cross_func, mut_func, elitism=elitism_flag)

                results.append((name, median_final))


print("\n📋 Mediana da fitness final (30 runs por combinação):\n")

for name, median in sorted(results, key=lambda x: x[1], reverse=True):
    print(f"{name:<60} -> {median:.4f}")



