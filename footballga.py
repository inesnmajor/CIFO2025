import random
import matplotlib as plt
from classes import Football

def runGA(self):
        print("Starting GA run...")
        self.initialize_population()

        for gen in range(self.generations):
            print(f"\n--- Generation {gen + 1} ---")
            fitnesses = [ind.fitness() for ind in self.population]
            self.best_scores.append(max(fitnesses))

            print(self.best_scores,":best score")
            
            best_gen = max(self.population, key=lambda s: s.fitness())
         
            if best_gen.fitness() > self.best_fitness:
                self.best_fitness = best_gen.fitness()
                self.best_solution = best_gen.deepcopy()

            new_population = []
            if self.elitism:
                elites = sorted(self.population, key=lambda s: -s.fitness())[:self.elite_size]
                print(f"Elitism: Copying {len(elites)} best individuals to new population")
                new_population.extend(elites)

            attempts = 0
            while len(new_population) < self.pop_size and attempts < self.max_attempts:
                print(f"New pop size: {len(new_population)} / {self.pop_size}")
                attempts += 1
                p1 = self.select_parent()
                p2 = self.select_parent()
                print("Selected parents")

                if random.random() < self.pc:
                    crossover_method = random.choice([
                        self.team_swap_crossover,
                        self.team_two_point_crossover
                    ])
                    c1, c2 = crossover_method(p1, p2)


                    # Aplica validações (ou fix_repr se quiseres)
                    if not self.is_unique(c1) or not self.is_unique(c2):
                        print("Filho descartado por repetição antes da mutação")
                        continue

                    if any(not team.is_valid() for team in c1.repr + c2.repr):
                        print("Filho inválido descartado")
                        continue

                    print("Applied crossover")
                else:
                    c1, c2 = p1.deepcopy(), p2.deepcopy()
                    print("Used replication")

                c1 = self.mutate_all(c1)
                c2 = self.mutate_all(c2)

                if not self.is_unique(c1) or not all(team.is_valid() for team in c1.repr):
                    print("Filho mutado c1 inválido")
                    continue
                if not self.is_unique(c2) or not all(team.is_valid() for team in c2.repr):
                    print("Filho mutado c2 inválido")
                    continue

                else:
                    print("Applied mutation")

                new_population.append(c1)
                if len(new_population) < self.pop_size:
                    new_population.append(c2)

            if attempts >= self.max_attempts:
                print(f"⚠️ Generation {gen+1}: broke after {self.max_attempts} attempts to create full population")

            self.population = new_population
            print(f"End of generation {gen + 1} | Best fitness so far: {self.best_fitness:.4f}")

def plot(self):
    plt.plot(self.best_scores)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("GA Performance Over Generations")
    plt.grid(True)
    plt.show()

def display_best_solution(self):
    if self.best_solution is None:
        print("\nNo valid solution found during the run.")
        return

    print("\nBest Score:", self.best_fitness)
    for i, team in enumerate(self.best_solution.repr):
        print(f"\nTeam {i + 1}:")
        for player in team.players:
            print(f"  {player['Name']} ({player['Position']}), Skill: {player['Skill']}, Cost: {player['Salary (€M)']}")

if __name__ == "__main__":
    ga = FootballGA(generations=90, pop_size=30, elite_size=2, selection_method="roulette", elitism=True, pc=0.9, pm=0.07)
    ga.run()
    ga.plot()
    ga.display_best_solution()