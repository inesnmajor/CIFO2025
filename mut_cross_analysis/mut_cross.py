import pandas as pd
import numpy as np
import csv
import json
from itertools import product
from library.selection import tournament_selection
from library.crossover import crossover_blockwise_teams, crossover_position_based
from library.crossover2child import crossover_blockwise_teams_two_offspring, crossover_position_based_two_offspring
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.GA import run_ga_test_single_child, run_ga_test_two_children


# ------------------ Fixed Parameters ------------------ #
SELECTION_METHOD = tournament_selection
CROSSOVER_PROB = 0.9
MUTATION_PROB = 0.1
GENERATIONS = 100
POP_SIZE = 40
N_RUNS = 30

# ------------------ Operators ------------------ #
crossover_methods = {
    "blockwise": (crossover_blockwise_teams, run_ga_test_single_child),
    "positionbased": (crossover_position_based, run_ga_test_single_child),
    "blockwise_2child": (crossover_blockwise_teams_two_offspring, run_ga_test_two_children),
    "positionbased_2child": (crossover_position_based_two_offspring, run_ga_test_two_children)
}

mutation_methods = {
    "global_perm": mutate_global_position_permutation,
    "random_swap": mutate_random_position_swap,
    "between_teams": mutate_swap_between_teams
}

elitism_options = [True, False]

# ------------------ Combinations ------------------ #
search_space = list(product(crossover_methods.items(), mutation_methods.items(), elitism_options))

# ------------------ Grid Search ------------------ #
results_df = pd.DataFrame()

for (c_name, (c_func, ga_runner)), (m_name, m_func), elitism in search_space:
    combination_label = f'{c_name}|{m_name}|elitism_{elitism}'
    print(f"\nRunning {combination_label} ...")

    all_runs = ga_runner(
        SELECTION_METHOD, c_func, m_func,
        generations=GENERATIONS,
        pop_size=POP_SIZE,
        n_runs=N_RUNS,
        elitism=elitism,
        crossover_prob=CROSSOVER_PROB,
        mutation_prob=MUTATION_PROB
    )

   
    all_runs_transposed = np.transpose(all_runs)

    
    generation_results = [[float(val) for val in gen_values] for gen_values in all_runs_transposed]

    results_df[combination_label] = generation_results

# ------------------ Save Results ------------------ #
results_df.to_csv('ga_grid_search_results.csv', quoting=csv.QUOTE_NONNUMERIC, index=False)
print("\nResults saved in 'ga_grid_search_results.csv'")

