# import pandas as pd
# players_df = pd.read_csv(r"C:\Users\inesm\OneDrive\Documentos\GitHub\CIFO2025\data\players(in).csv")

# POSITIONS = ["GK", "DEF", "MID", "FWD"]
# TEAM_STRUCTURE = {"GK": 1, "DEF": 2, "MID": 2, "FWD": 2}
# TEAM_SIZE = 7
# N_TEAMS = 5
# MAX_BUDGET = 750


import pandas as pd
import os

paths = [
    r"C:\Users\inesm\OneDrive\Documentos\GitHub\CIFO2025\data\players(in).csv",
    r"C:\Users\rodri\Desktop\Nova IMS\1ano\2nd Semester\Computational Intelligence for Otimization\CIFO2025\data\players(in).csv",
    ### ADICIONAR PATHS
    "data/players(in).csv",
    "../data/players(in).csv"
]

players_df = None
for path in paths:
    if os.path.exists(path):
        try:
            players_df = pd.read_csv(path)
            print(f"[INFO] Dataset carregado com sucesso de: {path}")
            break
        except Exception as e:
            print(f"[ERRO] Falha ao ler o ficheiro em: {path}\n{e}")

if players_df is None:
    raise FileNotFoundError("Não foi possível encontrar o ficheiro players(in).csv nos caminhos especificados.")

POSITIONS = ["GK", "DEF", "MID", "FWD"]
TEAM_STRUCTURE = {"GK": 1, "DEF": 2, "MID": 2, "FWD": 2}
TEAM_SIZE = 7
N_TEAMS = 5
MAX_BUDGET = 750