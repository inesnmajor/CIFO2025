from library.selection import tournament_selection, fitness_proportionate_selection
from library.crossover import *
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team
from library.constraints import check_no_duplicates, check_team_size, check_budget

import random
import numpy as np
from copy import deepcopy
import pandas as pd
from functools import partial


# Combinações possíveis
selection_methods = {
    "tournament": tournament_selection,
    "fitness_proportionate": fitness_proportionate_selection
}

crossover_methods = {
    "crossover_by_team_with_repair": crossover_by_team_with_repair,
    "crossover_by_position": crossover_by_position
}

mutation_methods = {
    "global_perm": mutate_global_position_permutation,
    "random_swap": mutate_random_position_swap,
    "between_teams": mutate_swap_between_teams
}


def run_ga_test(selection_func, crossover_func, mutation_func,
                generations=100, pop_size=40, elitism=True, n_runs=30,
                crossover_prob=0.9, mutation_prob=0.3):

    all_runs_best_per_gen = []

    for run in range(n_runs):
        population = [FootballSolution() for _ in range(pop_size)]
        best_per_gen = []

        for gen in range(generations):
            new_population = []

            if elitism:
                elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
                new_population.append(elite)

            while len(new_population) < pop_size:
                p1 = selection_func(population)
                p2 = selection_func(population)

                if random.random() < crossover_prob:
                    c1, c2 = crossover_func(p1, p2)
                else:
                    c1, c2 = deepcopy(p1), deepcopy(p2)

                # Verifica restrições após crossover
                for i, child in enumerate([c1, c2], start=1):
                    print(f"\n[DEBUG] Filho {i} após crossover (run {run+1}, gen {gen+1}):")
                    check_no_duplicates(child)
                    check_team_size(child)
                    check_budget(child)

                if random.random() < mutation_prob:
                    c1 = mutation_func(None, c1)
                if random.random() < mutation_prob:
                    c2 = mutation_func(None, c2)

                # Verifica restrições após mutação
                for i, child in enumerate([c1, c2], start=1):
                    print(f"\n[DEBUG] Filho {i} após mutação (run {run+1}, gen {gen+1}):")
                    check_no_duplicates(child)
                    check_team_size(child)
                    check_budget(child)

                for child in [c1, c2]:
                    if len(new_population) < pop_size:
                        new_population.append(child)

            population = new_population
            best_gen_fitness = max(ind.fitness() for ind in population)
            best_per_gen.append(best_gen_fitness)

        all_runs_best_per_gen.append(best_per_gen)

    return all_runs_best_per_gen


# ----------- Corre todas as combinações ----------- #

results_df = pd.DataFrame()

for elitism_flag in [True, False]:
    for sel_name, sel_func in selection_methods.items():
        for cross_name, cross_func in crossover_methods.items():
            for mut_name, mut_func in mutation_methods.items():
                name = f"{sel_name}|{cross_name}|{mut_name}|elitism={elitism_flag}"
                print(f"\nRunning {name} ...")

                all_runs = run_ga_test(
                    sel_func, cross_func, mut_func,
                    generations=100,
                    pop_size=40,
                    n_runs=30,
                    elitism=elitism_flag,
                    crossover_prob=0.9,
                    mutation_prob=0.1
                )

                medians = np.median(np.transpose(all_runs), axis=1)
                results_df[name] = medians

results_df.to_csv("ga_selection_analysis.csv", index_label="Generation")
print("\nResultados salvos em 'ga_selection_analysis.csv'")






#------------------------------------------------
#------------------------------------------------
#                   Rodrigo
#------------------------------------------------
#------------------------------------------------



# from library.selection import tournament_selection, fitness_proportionate_selection
# from library.crossover import crossover_by_team_with_repair, crossover_by_position
# from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
# from library.classes import FootballSolution, Team
# from library.constraints import check_no_duplicates, check_team_size, check_budget

# import random
# import numpy as np
# from copy import deepcopy
# import pandas as pd

# # Combinações possíveis
# selection_methods = {
#     "tournament": tournament_selection,
#     "fitness_proportionate": fitness_proportionate_selection
# }

# crossover_methods = {
#     "crossover_by_team_with_repair": crossover_by_team_with_repair,
#     "crossover_by_position": crossover_by_position
# }

# mutation_methods = {
#     "global_perm": mutate_global_position_permutation,
#     "random_swap": mutate_random_position_swap,
#     "between_teams": mutate_swap_between_teams
# }

# def run_ga_test(selection_func, crossover_func, mutation_func,
#                 generations=100, pop_size=40, elitism=True, n_runs=30,
#                 crossover_prob=0.9, mutation_prob=0.3):

#     all_runs_best_per_gen = []

#     for run in range(n_runs):
#         population = [FootballSolution() for _ in range(pop_size)]
#         best_per_gen = []

#         for gen in range(generations):
#             new_population = []

#             if elitism:
#                 elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
#                 new_population.append(elite)

#             while len(new_population) < pop_size:
#                 p1 = selection_func(population)
#                 p2 = selection_func(population)

#                 children = []
#                 if random.random() < crossover_prob:
#                     child = crossover_func(p1, p2)
#                 else:
#                     child = deepcopy(p1)

#                 children.append(child)

#                 # Tenta adicionar outro filho (ex: deepcopy do segundo pai)
#                 if len(new_population) + 1 < pop_size:
#                     if random.random() < crossover_prob:
#                         backup_child = crossover_func(p2, p1)
#                     else:
#                         backup_child = deepcopy(p2)
#                     children.append(backup_child)

#                 for i, child in enumerate(children, start=1):
#                     print(f"\n[DEBUG] Filho {i} após crossover (run {run+1}, gen {gen+1}):")
#                     check_no_duplicates(child)
#                     check_team_size(child)
#                     check_budget(child)

#                     if random.random() < mutation_prob:
#                         child = mutation_func(None, child)

#                     print(f"\n[DEBUG] Filho {i} após mutação (run {run+1}, gen {gen+1}):")
#                     check_no_duplicates(child)
#                     check_team_size(child)
#                     check_budget(child)

#                     if len(new_population) < pop_size:
#                         new_population.append(child)

#             population = new_population
#             best_gen_fitness = max(ind.fitness() for ind in population)
#             best_per_gen.append(best_gen_fitness)

#         all_runs_best_per_gen.append(best_per_gen)

#     return all_runs_best_per_gen


# # ----------- Corre todas as combinações ----------- #

# results_df = pd.DataFrame()

# for elitism_flag in [True, False]:
#     for sel_name, sel_func in selection_methods.items():
#         for cross_name, cross_func in crossover_methods.items():
#             for mut_name, mut_func in mutation_methods.items():
#                 name = f"{sel_name}|{cross_name}|{mut_name}|elitism={elitism_flag}"
#                 print(f"\nRunning {name} ...")

#                 all_runs = run_ga_test(
#                     sel_func, cross_func, mut_func,
#                     generations=100,
#                     pop_size=40,
#                     n_runs=30,
#                     elitism=elitism_flag,
#                     crossover_prob=0.9,
#                     mutation_prob=0.1
#                 )

#                 medians = np.median(np.transpose(all_runs), axis=1)
#                 results_df[name] = medians

# results_df.to_csv("ga_selection_analysis.csv", index_label="Generation")
# print("\nResultados salvos em 'ga_selection_analysis.csv'")
