# CIFO2025
Sports League Optimization - Genetic Algorithms

## **Overview**

This project applies a Genetic Algorithm (GA) to solve a fantasy sports league team-assignment optimization problem.Given a pool of players (each with a position, skill rating and salary), the goal is to build a set of balanced teams under a salary cap, minimizing the standard deviation of average team skills.

**Project Structure**
```bash
CIFO2025/
├── data/
│   └── players(in).csv        # Player dataset: name, position, skill rating, salary
├── library/                   # Core GA implementation modules
│   ├── classes.py             # Data classes for Player, Team, League
│   ├── crossover.py           # Crossover operator #1
│   ├── crossover2child.py     # Crossover operator #2
│   ├── fixed_para.py          # GA parameters (population size, mutation rate, etc.)
│   ├── GA.py                  # Main GA loop (initialization, evaluation, evolution)
│   ├── mutation.py            # 3 mutation operators
│   └── selection.py           # 2 selection mechanisms
├── mut_cross_analysis/        # Mutation & crossover analysis
│   ├── analysis.ipynb         # Jupyter notebook: operator comparison experiments
│   ├── mut_cross.py           # Script to reproduce analysis
│   └── ga_grid_search_results.csv # Results of the grid search
├── selection_analysis/        # Selection mechanism analysis
│   ├── selection_analysis.ipynb  # Notebook: selection experiments
│   ├── ga_selection_analysis.py  # Script to reproduce analysis
│   └── ga_selection_analysis.csv # Results of the selection grid search
├── best_league.py             # Script: run GA and output best league configuration
├── CIFO_2024_2025_Project_Statement.pdf  # Project requirements & guidelines
└── README.md 
```

---

## Usage

1. **Inspect the Data**

Open data/players(in).csv to see the list of 35 players, each with:

Position: GK, DEF, MID, FWD

Skill rating: 0–100

Salary: in million €

2. **Configure GA Parameters**

Edit library/fixed_para.py to adjust:

Population size

Number of generations

Crossover & mutation rates

Salary cap (default: €750 M per team)

3. **Run the Genetic Algorithm for best league**
``` python
    python best_league.py
```

This will:

    Load the player dataset.

    Initialize a population of league configurations.

    Evolve over the specified number of generations.

    Print and save the best league (5 teams of 7 players each).

4. **Analyze Operators**

Mutation & Crossover
```python
    jupyter notebook mut_cross_analysis/analysis.ipynb
```
Compare the impact of different mutation and crossover operators on convergence speed and solution quality.

Selection Mechanisms
```python
    jupyter notebook selection_analysis/selection_analysis.ipynb
```
Evaluate tournament vs. roulette-wheel selection.

5. **Code Modules**

**classes.py** - Defines Player, Team and League classes, plus fitness evaluation (team skill SD + salary cap penalty).

**GA.py** - Implements the GA workflow: selection → crossover → mutation → replacement.

**mutation.py** - Contains at least three problem-adapted mutation operators.

**crossover.py & crossover2child.py** - Two distinct crossover strategies.

**selection.py** - Includes tournament selection, roulette-wheel selection.

5. **Results**

The best found league (skill standard deviation, salary feasibility, team rosters) is printed to console and saved in best_league_output.txt after each run of best_league.py. Use this to compare different GA settings.
