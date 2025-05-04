# from library.selection import tournament_selection, fitness_proportionate_selection
# from library.crossover import crossover_blockwise_teams, crossover_position_based
# from library.mutation import mutate_global_position_permutation, mutate_random_position_swap, mutate_swap_between_teams
# from library.classes import FootballSolution, Team

# import random
# import numpy as np
# from copy import deepcopy
# import csv
# import pandas as pd


# # possible combinations
# selection_methods = {
#     "tournament": tournament_selection,
#     "fitness_proportionate": fitness_proportionate_selection
# }

# crossover_methods = {
#     "blockwise": crossover_blockwise_teams,
#     "positionbased": crossover_position_based
# }

# mutation_methods = {
#     "global_perm": mutate_global_position_permutation,
#     "random_swap": mutate_random_position_swap,
#     "between_teams": mutate_swap_between_teams
# }

# '''
# function to run tests for choosing the best selection algorithm
# we will run 30 times and take the median to evaluate the best selection algorithm 
# we will use 30 generations and population size of 20 to run this tests-- FOR NOW--
# '''

# def run_ga_test(selection_func, crossover_func, mutation_func,
#                 generations=100, pop_size=40, elitism=True, n_runs=30,
#                 crossover_prob=0.9, mutation_prob=0.3):

#     all_runs_best_per_gen = []  #each element will be a list of fitnesses per generation

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

#                 if random.random() < crossover_prob:
#                     c1 = crossover_func(p1, p2)
#                 else:
#                     c1= deepcopy(p1)

#                 if random.random() < mutation_prob:
#                     c1 = mutation_func(None, c1)
#                 # if random.random() < mutation_prob:
#                 #     c2 = mutation_func(None, c2)

#                 for child in [c1]:
#                     if len(new_population) < pop_size:
#                         new_population.append(child)

#             population = new_population

#             # keeps the best fitness of this gen
#             best_gen_fitness = max(ind.fitness() for ind in population)
#             best_per_gen.append(best_gen_fitness)

#         all_runs_best_per_gen.append(best_per_gen)

#     return all_runs_best_per_gen  #list of lists




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
#                     mutation_prob=0.1,
    
#                 )

#                 #all_runs is a list of 30 lists, one per run
#                 medians = np.median(np.transpose(all_runs), axis=1)

#                 results_df[name] = medians

# saves the csv file
# results_df.to_csv("ga_selection_analysis.csv", index_label="Generation")

# print("\nResultados salvos em 'ga_selection_analysis.csv'")







#------------------------------------------------
#------------------------------------------------
#                   Rodrigo
#------------------------------------------------
#------------------------------------------------

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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

# def run_ga_test(selection_func, crossover_func, mutation_func,
#                 generations=100, pop_size=40, elitism=True, n_runs=1,
#                 crossover_prob=0.9, mutation_prob=0.3):

#     all_runs_best_per_gen = []

#     for run in range(n_runs):
#         print(f"\n--- RUN {run+1} ---")
#         population = [FootballSolution() for _ in range(pop_size)]
#         best_per_gen = []

#         for gen in range(generations):
#             print(f"\nGeneration {gen+1}")
#             new_population = []

#             if elitism:
#                 elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
#                 print(f"  Elitism ON: Best fitness from previous gen = {elite.fitness():.2f}")
#                 new_population.append(elite)

#             while len(new_population) < pop_size:
#                 p1 = selection_func(population)
#                 p2 = selection_func(population)
#                 print(f"  Selected parents (fitness): {p1.fitness():.2f}, {p2.fitness():.2f}")

#                 if random.random() < crossover_prob:
#                     c1 = crossover_func(p1, p2)
#                     print(f"    Crossover occurred.")
#                 else:
#                     c1 = deepcopy(p1)
#                     print(f"    Crossover skipped.")

#                 if random.random() < mutation_prob:
#                     c1 = mutation_func(None, c1)
#                     print(f"    Mutation applied.")
#                 else:
#                     print(f"    Mutation skipped.")

#                 if len(new_population) < pop_size:
#                     new_population.append(c1)

#             population = new_population

#             best_gen_fitness = max(ind.fitness() for ind in population)
#             print(f"  Best fitness this generation: {best_gen_fitness:.2f}")
#             best_per_gen.append(best_gen_fitness)

#         all_runs_best_per_gen.append(best_per_gen)

#     return all_runs_best_per_gen





# results_df = pd.DataFrame()

# for elitism_flag in [True]:#, False]:
#     print(f"\n==============================")
#     print(f"ELITISM = {elitism_flag}")
#     print(f"==============================")

#     for sel_name, sel_func in selection_methods.items():
#         for cross_name, cross_func in crossover_methods.items():
#             for mut_name, mut_func in mutation_methods.items():
#                 name = f"{sel_name}|{cross_name}|{mut_name}|elitism={elitism_flag}"
#                 print(f"\n--- Running configuration: {name} ---")

#                 all_runs = run_ga_test(
#                     sel_func, cross_func, mut_func,
#                     generations=2,
#                     pop_size=40,
#                     n_runs=1,  # coloca 1 para debug, depois metes 30
#                     elitism=elitism_flag,
#                     crossover_prob=0.9,
#                     mutation_prob=0.1,
#                 )

#                 # Transpõe para obter fitness por geração
#                 medians = np.median(np.transpose(all_runs), axis=1)

#                 print(f"  Final fitness (última geração): {medians[-1]:.2f}")
#                 print(f"  Melhor fitness (global): {max(medians):.2f}")
#                 print(f"  Geração com melhor fitness: {np.argmax(medians) + 1}")

#                 results_df[name] = medians




def run_ga_test_debug(selection_func, crossover_func, mutation_func,
                      generations=3, pop_size=6, elitism=True, n_runs=1,
                      crossover_prob=0.9, mutation_prob=0.3):
    from collections import Counter

    def summarize_population(pop):
        fitnesses = [ind.fitness() for ind in pop]
        return {
            'max': np.max(fitnesses),
            'min': np.min(fitnesses),
            'mean': np.mean(fitnesses),
            'std': np.std(fitnesses),
            'top3': sorted(fitnesses, reverse=True)[:3]
        }

    all_runs_best_per_gen = []

    for run in range(n_runs):
        print(f"\n========== RUN {run + 1} ==========")
        population = [FootballSolution() for _ in range(pop_size)]
        best_per_gen = []

        print("\nInitial Population:")
        for i, ind in enumerate(population):
            print(f"  Ind {i}: fitness = {ind.fitness():.4f}")

        for gen in range(generations):
            print(f"\n------ Generation {gen + 1} ------")
            new_population = []

            if elitism:
                elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
                print(f"  [Elitism] Best individual carried: fitness = {elite.fitness():.4f}")
                # elite.summary()
                elite_fingerprint = elite.get_fingerprint()
                new_population.append(elite)

            added_child = False

            while len(new_population) < pop_size:
                p1 = selection_func(population)
                p2 = selection_func(population)
                print(f"\n  Parents selected: fitness = {p1.fitness():.4f}, {p2.fitness():.4f}")

                if random.random() < crossover_prob:
                    child = crossover_func(p1, p2)
                    print("    > Crossover applied")
                else:
                    child = deepcopy(p1)
                    print("    > Crossover skipped (copy of p1)")

                if random.random() < mutation_prob:
                    before = child.fitness()
                    child = mutation_func(None, child)
                    after = child.fitness()
                    print(f"    > Mutation applied: fitness {before:.4f} → {after:.4f}")
                else:
                    print("    > Mutation skipped")

                new_population.append(child)

                if not added_child:
                    print("    > Child summary:")
                    # child.summary()
                    added_child = True

            # Fitness stats
            fitness_stats = summarize_population(new_population)
            print("\n  [Stats] New population fitness:")
            print(f"    Max: {fitness_stats['max']:.4f}")
            print(f"    Min: {fitness_stats['min']:.4f}")
            print(f"    Mean: {fitness_stats['mean']:.4f}")
            print(f"    Std: {fitness_stats['std']:.4f}")
            print(f"    Top 3: {', '.join(f'{x:.4f}' for x in fitness_stats['top3'])}")

            # Check for duplicates
            fingerprints = [str(ind.get_fingerprint()) for ind in new_population]
            count_dups = sum(v > 1 for v in Counter(fingerprints).values())
            print(f"    Duplicates in population: {count_dups}")

            # Confirmar se elite sobreviveu
            if elitism:
                elite_found = any(ind.get_fingerprint() == elite_fingerprint for ind in new_population)
                print(f"    Elite preserved in new population? {'✅ Yes' if elite_found else '❌ No'}")

            population = new_population
            best_fitness = max(ind.fitness() for ind in population)
            best_per_gen.append(best_fitness)
            print(f"  [Best of Generation] Fitness: {best_fitness:.4f}")

        all_runs_best_per_gen.append(best_per_gen)

    return all_runs_best_per_gen




run_ga_test_debug(
    selection_func=tournament_selection,
    crossover_func=crossover_position_based,
    mutation_func=mutate_swap_between_teams,
    generations=3,
    pop_size=20,
    elitism=True,
    n_runs=1,
    crossover_prob=0.9,
    mutation_prob=0.1,
)

