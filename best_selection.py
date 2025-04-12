from library.selection import tournament_selection, fitness_proportionate_selection
from library.crossover import team_swap_crossover, team_two_point_crossover
from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
from library.classes import FootballSolution, Team

import random
import numpy as np
from copy import deepcopy

# possible combinations
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

'''
function to run tests for choosing the best selection algorithm
we will run 30 times and take the median to evaluate the best selection algorithm 
we will use 30 generations and population size of 20 to run this tests-- FOR NOW--
'''
def run_ga_test(selection_func, crossover_func, mutation_func,
                generations=30, pop_size=20, elitism=True, n_runs=15,
                crossover_prob=0.9, mutation_prob=0.3):
    
    final_best_fitnesses = []

    for run in range(n_runs):
        population = [FootballSolution() for _ in range(pop_size)] #create a population of solutions
        
        for gen in range(generations):
            new_population = []

            if elitism:
                elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
                new_population.append(elite)

            while len(new_population) < pop_size:
                p1 = selection_func(population)
                p2 = selection_func(population)

                if random.random() < crossover_prob:
                    c1, c2 = crossover_func(None, p1, p2)
                else:
                    c1, c2 = deepcopy(p1), deepcopy(p2)

                if random.random() < mutation_prob:
                    c1 = mutation_func(None, c1)
                if random.random() < mutation_prob:
                    c2 = mutation_func(None, c2)

                for child in [c1, c2]:
                    if len(new_population) < pop_size:
                        new_population.append(child)

            population = new_population


        # saves best fitness
        final_best = max(ind.fitness() for ind in population)
        final_best_fitnesses.append(final_best)

    # median
    return np.median(final_best_fitnesses), final_best_fitnesses



results = []
'''
loop of all possible combinations of elitism, selection algorithms, crossover, and mutations
'''
for elitism_flag in [True, False]:
    for sel_name, sel_func in selection_methods.items():
        for cross_name, cross_func in crossover_methods.items():
            for mut_name, mut_func in mutation_methods.items():
                name = f"{sel_name}|{cross_name}|{mut_name}|elitism={elitism_flag}"
                print(f"\nRunning {name} ...")

                median_final, all_finals = run_ga_test(
                    sel_func, cross_func, mut_func,
                    elitism=elitism_flag,
                    crossover_prob=0.9,
                    mutation_prob=0.1
                )

                results.append((name, median_final))


print("Median of final fitness: 30 runs per combination\n")

for name, median in sorted(results, key=lambda x: x[1], reverse=True):
    print(f"{name:<60} -> {median:.4f}")



