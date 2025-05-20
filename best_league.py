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

def run_ga_test_two_children_return_best(selection_func, crossover_func, mutation_func,
                                         generations=100, pop_size=40, elitism=True,
                                         crossover_prob=0.9, mutation_prob=0.1):
    """
    runs a GA and returns the best solution found (with the best combination found on grid search and the one that peaked 
    earlier).
    """
    from copy import deepcopy
    import random

    population = [FootballSolution() for _ in range(pop_size)]

    for gen in range(generations):
        new_population = []

        if elitism:
            elite = deepcopy(max(population, key=lambda ind: ind.fitness()))
            new_population.append(elite)

        while len(new_population) < pop_size:
            p1 = selection_func(population)
            p2 = selection_func(population)

            # Crossover (two children)
            if random.random() < crossover_prob:
                child1, child2 = crossover_func(p1, p2)
            else:
                child1, child2 = deepcopy(p1), deepcopy(p2)

            # Mutation on both
            if random.random() < mutation_prob:
                child1 = mutation_func(None, child1)
            if random.random() < mutation_prob:
                child2 = mutation_func(None, child2)

            for child in [child1, child2]:
                if len(new_population) < pop_size:
                    new_population.append(child)

        population = new_population

    # Return the best individual from the final population
    best_solution = max(population, key=lambda ind: ind.fitness())
    return best_solution

best_solution = run_ga_test_two_children_return_best(
    selection_func=tournament_selection,
    crossover_func=crossover_blockwise_teams_two_offspring,
    mutation_func=mutate_global_position_permutation,
    generations=50,
    pop_size=40,
    elitism=True,
    crossover_prob=0.9,
    mutation_prob=0.1
)

print(best_solution)

for team in best_solution.repr:
    print(team)

def save_solution_to_file(solution, filepath="best_league.txt"):
    """
    Saves on a txt file the global league summary first, followed by each team individually.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        # Write the overall league representation
        f.write("=== League Overview ===\n")
        f.write(str(solution) + "\n\n")

        # Write each team individually 
        f.write("=== Individual Teams ===\n")
        for team_idx, team in enumerate(solution.repr, start=1):
            f.write(f"\nTeam {team_idx}:\n")
            f.write(str(team) + "\n") 

    print(f"Solution with league and team details saved to {filepath}")

save_solution_to_file(best_solution, "best_league.txt")


