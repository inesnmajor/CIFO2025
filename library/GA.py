from library.classes import FootballSolution, Team

import random
import numpy as np
from copy import deepcopy
import csv
import pandas as pd

def run_ga_test_single_child(selection_func, crossover_func, mutation_func,
                             generations=100, pop_size=40, elitism=True, n_runs=30,
                             crossover_prob=0.9, mutation_prob=0.1): #default settings
    """
    Runs a GA test assuming crossover produces a single child.
    """
    from copy import deepcopy
    import random

    all_runs_best_per_gen = []

    for run in range(n_runs): #loop for runs
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

                # Crossover (single child)
                if random.random() < crossover_prob:
                    child = crossover_func(p1, p2)
                else:
                    child = deepcopy(p1)

                # Mutation
                if random.random() < mutation_prob:
                    child = mutation_func(None, child)

                new_population.append(child)

            population = new_population
            best_gen_fitness = max(ind.fitness() for ind in population)
            best_per_gen.append(best_gen_fitness)

        all_runs_best_per_gen.append(best_per_gen)

    return all_runs_best_per_gen # Returns a list of length n_runs, where each element is a list of the best fitness value
# found in each generation (i.e. an n_runs × generations matrix of max fitness scores)


def run_ga_test_two_children(selection_func, crossover_func, mutation_func,
                             generations=100, pop_size=40, elitism=True, n_runs=30,
                             crossover_prob=0.9, mutation_prob=0.1): #defauts
    """
    Runs a GA test assuming crossover produces two children.
    """
    from copy import deepcopy
    import random

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
            best_gen_fitness = max(ind.fitness() for ind in population)
            best_per_gen.append(best_gen_fitness)

        all_runs_best_per_gen.append(best_per_gen) 

    return all_runs_best_per_gen # Returns a list of length n_runs, where each element is a list of the best fitness value
# found in each generation (i.e. an n_runs × generations matrix of max fitness scores)

