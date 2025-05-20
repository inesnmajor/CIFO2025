from library.selection import tournament_selection, fitness_proportionate_selection

from library.crossover import crossover_blockwise_teams, crossover_position_based
from library.crossover2child import crossover_blockwise_teams_two_offspring, crossover_position_based_two_offspring

from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team
from library.GA import run_ga_test_single_child, run_ga_test_two_children

import random
import numpy as np
from copy import deepcopy
import csv
import pandas as pd
from itertools import product


# ------------------ Operators ------------------ #
selection_methods = {
    "tournament": tournament_selection,
    "fitness_proportionate": fitness_proportionate_selection
}

crossover_methods_single_child = {
    "blockwise": crossover_blockwise_teams,
    "positionbased": crossover_position_based
}

crossover_methods_two_children = {
    "blockwise_2child": crossover_blockwise_teams_two_offspring,
    "positionbased_2child": crossover_position_based_two_offspring
}

mutation_methods = {
    "global_perm": mutate_global_position_permutation,
    "random_swap": mutate_random_position_swap,
    "between_teams": mutate_swap_between_teams
}

# ------------------ Combinations ------------------ #
all_xo_mut_combinations = list(product(
    list(crossover_methods_single_child.items()) + list(crossover_methods_two_children.items()),
    mutation_methods.items()
))
xo_mut_comb_sample = random.sample(all_xo_mut_combinations, 6) #decided to go with only 6 to run in an effective time

selection_combs = []
for sel_name, sel_func in selection_methods.items():
    for (c_name, c_func), (m_name, m_func) in xo_mut_comb_sample:
        ga_runner = run_ga_test_two_children if "2child" in c_name else run_ga_test_single_child
        selection_combs.append((sel_name, sel_func, c_name, c_func, m_name, m_func, ga_runner))



# ------------------ Fixed Parameters ------------------ #
generations = 100
pop_size = 40
n_runs = 30
crossover_prob = 0.9
mutation_prob = 0.1


results_df = pd.DataFrame()


# ------------------ Grid Search ------------------ #
for sel_name, sel_func, c_name, c_func, m_name, m_func, ga_runner in selection_combs:
    combination_name = f'{sel_name}|{c_name}|{m_name}|elitism=True'
    print(f"\nRunning {combination_name} ...")

    all_runs = ga_runner(
        sel_func, c_func, m_func,
        generations=generations,
        pop_size=pop_size,
        n_runs=n_runs,
        elitism=True,
        crossover_prob=crossover_prob,
        mutation_prob=mutation_prob
    )

    medians = np.median(np.transpose(all_runs), axis=1)
    results_df[combination_name] = medians

# ------------------ Results ------------------ #
results_df.to_csv('ga_selection_analysis.csv')
print("\nResults saved 'ga_selection_analysis.csv'")




