import pandas as pd
import os

paths = [
    r"C:\Users\inesm\OneDrive\Documentos\GitHub\CIFO2025\data\players(in).csv",
    r"C:\Users\rodri\Desktop\Nova IMS\1ano\2nd Semester\Computational Intelligence for Otimization\CIFO2025\data\players(in).csv",
    r"C:\Users\pedro\Documentos\GitHub\CIFO2025\data\players(in).csv"
    r"C:\Users\luis\Documentos\mestrado\GitHub\CIFO2025\data\players(in).csv"
]

players_df = None
for path in paths:
    if os.path.exists(path):
        try:
            players_df = pd.read_csv(path)
            print(f"dataset load from: {path}")
            break
        except Exception as e:
            print(f"error while reading from: {path}\n{e}")

if players_df is None:
    raise FileNotFoundError("not able to find the file")

POSITIONS = ["GK", "DEF", "MID", "FWD"]
TEAM_STRUCTURE = {"GK": 1, "DEF": 2, "MID": 2, "FWD": 2}
TEAM_SIZE = 7
N_TEAMS = 5
MAX_BUDGET = 750