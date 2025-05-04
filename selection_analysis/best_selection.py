from library.selection import tournament_selection, fitness_proportionate_selection
from library.crossover import crossover_blockwise_teams, crossover_position_based
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team

import random
import numpy as np
from copy import deepcopy
import csv
import pandas as pd


# possible combinations
selection_methods = {
    "tournament": tournament_selection,
    "fitness_proportionate": fitness_proportionate_selection
}

crossover_methods = {
    "blockwise": crossover_blockwise_teams,
    "positionbased": crossover_position_based
}

mutation_methods = {
    "global_perm": mutate_global_position_permutation,
    "random_swap": mutate_random_position_swap,
    "between_teams": mutate_swap_between_teams
}

'''
function to run tests for choosing the best selection algorithm
we will run 30 times and take the median to evaluate the best selection algorithm 
we will use 30 generations and population size of 20 to run this tests-- FOR NOW--
'''

def run_ga_test(selection_func, crossover_func, mutation_func,
                generations=100, pop_size=40, elitism=True, n_runs=30,
                crossover_prob=0.9, mutation_prob=0.3):

    all_runs_best_per_gen = []  #each element will be a list of fitnesses per generation

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
                    c1 = crossover_func(p1, p2)
                else:
                    c1= deepcopy(p1)

                if random.random() < mutation_prob:
                    c1 = mutation_func(None, c1)
                # if random.random() < mutation_prob:
                #     c2 = mutation_func(None, c2)

                for child in [c1]:
                    if len(new_population) < pop_size:
                        new_population.append(child)

            population = new_population

            # keeps the best fitness of this gen
            best_gen_fitness = max(ind.fitness() for ind in population)
            best_per_gen.append(best_gen_fitness)

        all_runs_best_per_gen.append(best_per_gen)

    return all_runs_best_per_gen  #list of lists




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
                    mutation_prob=0.1,
    
                )

                #all_runs is a list of 30 lists, one per run
                medians = np.median(np.transpose(all_runs), axis=1)

                results_df[name] = medians

# saves the csv file
results_df.to_csv("ga_selection_analysis.csv", index_label="Generation")

print("\nResultados salvos em 'ga_selection_analysis.csv'")





