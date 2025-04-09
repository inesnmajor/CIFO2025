import pandas as pd
players_df = pd.read_csv(r"C:\Users\inesm\OneDrive\Documentos\GitHub\CIFO2025\data\players(in).csv")

POSITIONS = ["GK", "DEF", "MID", "FWD"]
TEAM_STRUCTURE = {"GK": 1, "DEF": 2, "MID": 2, "FWD": 2}
TEAM_SIZE = 7
N_TEAMS = 5
MAX_BUDGET = 750