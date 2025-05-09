from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df,MAX_BUDGET
import random
import numpy as np

def crossover_position_based_explained_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    # Preparar estruturas para os dois filhos
    offspring_teams_1 = []
    offspring_teams_2 = []
    used_names_1 = set()
    used_names_2 = set()

    print("\n===== [INÍCIO] Crossover baseado em posição para DOIS FILHOS =====")

    for team_idx in range(N_TEAMS):
        for offspring_label, offspring_teams, used_names in [
            ("Filho 1", offspring_teams_1, used_names_1),
            ("Filho 2", offspring_teams_2, used_names_2)
        ]:
            print(f"\n\n=== [{offspring_label} - EQUIPA {team_idx+1}] ===")
            team_players = []

            # Agrupar jogadores dos pais por posição
            position_pool = {pos: [] for pos in expected_structure}
            for parent_label, parent in zip(['p1', 'p2'], [p1, p2]):
                print(f"\n- A ler equipa {team_idx+1} do {parent_label}:")
                for player in parent.repr[team_idx].players:
                    print(f"  → {player['Name']} ({player['Position']}) disponível")
                    position_pool[player['Position']].append(player)

            for pos, n_needed in expected_structure.items():
                print(f"\n🎯 Selecionar {n_needed} jogadores para posição {pos}")
                selected = []
                pool = position_pool[pos]
                random.shuffle(pool)

                print(f"  📦 Pool inicial ({len(pool)} jogadores): {[p['Name'] for p in pool]}")
                print(f"  🚫 Nomes já usados: {sorted(used_names)}")

                # Tentar escolher do pool
                for p in pool:
                    if p['Name'] in used_names:
                        print(f"    ⛔ {p['Name']} já foi usado noutra equipa — ignorado")
                        continue
                    selected.append(p)
                    used_names.add(p['Name'])
                    print(f"    ✅ {p['Name']} escolhido do pai")
                    if len(selected) == n_needed:
                        break

                # Se ainda faltar
                if len(selected) < n_needed:
                    faltam = n_needed - len(selected)
                    print(f"    ⚠️ Faltam {faltam} jogadores → procurar no dataset")
                    available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                    random.shuffle(available)
                    for p in available:
                        selected.append(p)
                        used_names.add(p['Name'])
                        print(f"    🟡 {p['Name']} escolhido do dataset")
                        if len(selected) == n_needed:
                            break

                if len(selected) < n_needed:
                    print(f"[❌ ERRO] Não foi possível preencher {n_needed} jogadores da posição {pos} no {offspring_label}")
                    raise SystemExit(f"Violação da estrutura mesmo após usar o dataset no {offspring_label}.")

                team_players.extend(selected)

            print(f"\n✅ {offspring_label} - Equipa {team_idx+1} criada com:")
            for p in team_players:
                print(f"  - {p['Name']} ({p['Position']})")

            offspring_teams.append(Team(team_players))
            print(f"🔒 used_names atualizado: {sorted(used_names)}")

    print("\n===== [FINAL] Dois filhos criados com 5 equipas cada sem duplicados =====")
    print(f"[Filho 1] Jogadores únicos: {len(used_names_1)}")
    print(f"[Filho 2] Jogadores únicos: {len(used_names_2)}")

    return (
        FootballSolution(offspring_teams_1, players_df),
        FootballSolution(offspring_teams_2, players_df)
    )

def crossover_position_based_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    offspring_teams_1 = []
    offspring_teams_2 = []
    used_names_1 = set()
    used_names_2 = set()

    for team_idx in range(N_TEAMS):
        for offspring_label, offspring_teams, used_names in [
            ("Filho 1", offspring_teams_1, used_names_1),
            ("Filho 2", offspring_teams_2, used_names_2)
        ]:
            team_players = []
            position_pool = {pos: [] for pos in expected_structure}
            
            # Pool from parents
            for parent in [p1, p2]:
                for player in parent.repr[team_idx].players:
                    position_pool[player['Position']].append(player)

            for pos, n_needed in expected_structure.items():
                selected = []
                pool = position_pool[pos]
                random.shuffle(pool)

                # Select from parents
                for p in pool:
                    if p['Name'] in used_names:
                        continue
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

                # Fill with dataset if needed
                if len(selected) < n_needed:
                    available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                    random.shuffle(available)
                    for p in available:
                        selected.append(p)
                        used_names.add(p['Name'])
                        if len(selected) == n_needed:
                            break

                if len(selected) < n_needed:
                    raise SystemExit(f"[{offspring_label}] Violação da estrutura na equipa {team_idx+1}")

                team_players.extend(selected)

            offspring_teams.append(Team(team_players))

    return (
        FootballSolution(offspring_teams_1, players_df),
        FootballSolution(offspring_teams_2, players_df)
    )

######################################_------------------------------------------------------------------------------------------------

def crossover_blockwise_teams_explained_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    """
    Crossover por blocos com explicações, gerando DOIS filhos.
    Cada filho recebe equipas aleatórias dos pais, evitando duplicados e completando com o dataset se necessário.
    """
    from copy import deepcopy
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    def generate_offspring(label):
        print(f"\n===== [INÍCIO] {label} =====")
        used_names = set()
        offspring_teams = []

        n_from_p1 = random.randint(2, 3)
        p1_indices = random.sample(range(N_TEAMS), n_from_p1)
        p2_indices = [i for i in range(N_TEAMS) if i not in p1_indices]

        print(f"🎲 {label} - Equipas herdadas: {n_from_p1} do p1 → {p1_indices} | {N_TEAMS - n_from_p1} do p2 → {p2_indices}")

        for idx in p1_indices + p2_indices:
            source = p1 if idx in p1_indices else p2
            print(f"\n🧬 {label} - A copiar equipa {idx+1} do {'p1' if idx in p1_indices else 'p2'}...")
            raw_players = deepcopy(source.repr[idx].players)
            team_players = []

            for p in raw_players:
                if p['Name'] in used_names:
                    print(f"    ⛔ {p['Name']} já foi usado noutra equipa — ignorado")
                else:
                    print(f"    ✅ {p['Name']} copiado")
                    team_players.append(p)
                    used_names.add(p['Name'])

            if len(team_players) < TEAM_SIZE:
                print(f"    ⚠️ Equipa incompleta (tem {len(team_players)} jogadores), a preencher...")
                pos_counts = Counter(p['Position'] for p in team_players)
                pos_missing = {pos: expected_structure[pos] - pos_counts.get(pos, 0) for pos in expected_structure}
                for pos, count in pos_missing.items():
                    if count > 0:
                        available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                        random.shuffle(available)
                        for p in available[:count]:
                            print(f"    🟡 {p['Name']} ({p['Position']}) adicionado do dataset")
                            team_players.append(p)
                            used_names.add(p['Name'])

            print(f"  ✅ Equipa final criada com: {[p['Name'] for p in team_players]}")
            offspring_teams.append(Team(team_players))

        print(f"===== [FINAL] {label} - Solução construída com 5 equipas =====")
        return FootballSolution(offspring_teams, players_df)

    return generate_offspring("Filho 1"), generate_offspring("Filho 2")



def crossover_blockwise_teams_two_offspring(p1: FootballSolution, p2: FootballSolution) -> tuple[FootballSolution, FootballSolution]:
    from copy import deepcopy
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())

    def generate_offspring():
        used_names = set()
        offspring_teams = []
        n_from_p1 = random.randint(2, 3)
        p1_indices = random.sample(range(N_TEAMS), n_from_p1)
        p2_indices = [i for i in range(N_TEAMS) if i not in p1_indices]

        for idx in p1_indices + p2_indices:
            source = p1 if idx in p1_indices else p2
            raw_players = deepcopy(source.repr[idx].players)
            team_players = [p for p in raw_players if p['Name'] not in used_names]
            used_names.update(p['Name'] for p in team_players)

            if len(team_players) < TEAM_SIZE:
                pos_counts = Counter(p['Position'] for p in team_players)
                pos_missing = {pos: expected_structure[pos] - pos_counts.get(pos, 0) for pos in expected_structure}
                for pos, count in pos_missing.items():
                    if count > 0:
                        available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                        random.shuffle(available)
                        team_players.extend(available[:count])
                        used_names.update(p['Name'] for p in available[:count])

            offspring_teams.append(Team(team_players))
        return FootballSolution(offspring_teams, players_df)

    return generate_offspring(), generate_offspring()
