from copy import deepcopy
from collections import Counter
from library.classes import FootballSolution, Team
from library.fixed_para import POSITIONS, TEAM_STRUCTURE, N_TEAMS,TEAM_SIZE, players_df,MAX_BUDGET
import random
import numpy as np

def crossover_by_team_with_repair(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Team-wise crossover: randomly pick teams from parents, 
    repair duplicates and missing players, and fix budget violations if needed.
    """
    offspring_teams = []
    used_names = set()

    # Step 1: Randomly select teams from parents
    for i in range(N_TEAMS):
        team_source = p1 if random.random() < 0.5 else p2
        team = deepcopy(team_source.repr[i])
        offspring_teams.append(team)
        used_names.update(p['Name'] for p in team.players)

    # Step 2: Detect and remove duplicate players
    all_players = [p['Name'] for team in offspring_teams for p in team.players]
    name_counts = Counter(all_players)
    duplicates = [name for name, count in name_counts.items() if count > 1]

    for name in duplicates:
        found_once = False
        for team in offspring_teams:
            new_players = []
            for p in team.players:
                if p['Name'] == name:
                    if not found_once:
                        new_players.append(p)
                        found_once = True  # Keep first occurrence
                else:
                    new_players.append(p)
            team.players = new_players

    # Step 3: Fill missing players
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(players_df['Name'])
    all_used = {p['Name'] for team in offspring_teams for p in team.players}
    missing_names = list(all_names - all_used)

    for name in missing_names:
        player = name_to_player[name]
        for team in offspring_teams:
            pos = player['Position']
            pos_count = sum(1 for p in team.players if p['Position'] == pos)
            if len(team.players) < TEAM_SIZE and pos_count < TEAM_STRUCTURE[pos]:
                team.players.append(player)
                break

    # Step 4: Fix overbudget teams (new!)
    for team in offspring_teams:
        if team.total_salary() > MAX_BUDGET:
            # Find cheaper players to replace expensive ones
            available_players = [
                p for p in players_df.to_dict('records')
                if p['Name'] not in {pl['Name'] for t in offspring_teams for pl in t.players}
            ]

            for _ in range(5):  # attempt up to 5 replacements per team
                most_expensive = max(team.players, key=lambda p: float(p['Salary (€M)']))
                pos = most_expensive['Position']

                # Find cheaper candidates with the same position
                cheaper_candidates = [p for p in available_players if p['Position'] == pos and p['Salary (€M)'] < most_expensive['Salary (€M)']]

                if not cheaper_candidates:
                    break  # no cheaper replacement found

                replacement = random.choice(cheaper_candidates)
                team.players = [p for p in team.players if p['Name'] != most_expensive['Name']]

                team.players.append(replacement)

                available_players.remove(replacement)

                if team.total_salary() <= MAX_BUDGET:
                    break  # team budget is now okay

    # Step 5: Return final offspring
    if all(team.is_valid() for team in offspring_teams):
        return FootballSolution(offspring_teams, players_df)
    else:
        return deepcopy(p1)  # fallback if fixing fails


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


def crossover_teamwise_mix_and_repair(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Team-wise crossover: mixes players team by team from each parent,
    repairs duplicates and fills missing slots, without forcing budget compliance.
    Overbudget teams are allowed but will receive low fitness.
    """
    offspring_teams = []
    used_names = set()

    # Step 1: Mix players from each team (half from each parent)
    for i in range(N_TEAMS):
        team1_players = deepcopy(p1.repr[i].players)
        team2_players = deepcopy(p2.repr[i].players)

        random.shuffle(team1_players)
        random.shuffle(team2_players)

        half = TEAM_SIZE // 2
        team_players = team1_players[:half] + team2_players[TEAM_SIZE - half:]
        offspring_teams.append(Team(team_players))
        used_names.update(p['Name'] for p in team_players)

    # Step 2: Remove duplicate players (only keep first occurrence)
    all_players = [p['Name'] for team in offspring_teams for p in team.players]
    name_counts = Counter(all_players)
    duplicates = [name for name, count in name_counts.items() if count > 1]

    for name in duplicates:
        found_once = False
        for team in offspring_teams:
            new_players = []
            for p in team.players:
                if p['Name'] == name:
                    if not found_once:
                        new_players.append(p)
                        found_once = True
                else:
                    new_players.append(p)
            team.players = new_players

    # Step 3: Fill missing players to reach 7 per team and correct position structure
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(players_df['Name'])
    all_used = {p['Name'] for team in offspring_teams for p in team.players}
    missing_names = list(all_names - all_used)

    for name in missing_names:
        player = name_to_player[name]
        for team in offspring_teams:
            pos = player['Position']
            pos_count = sum(1 for p in team.players if p['Position'] == pos)
            if len(team.players) < TEAM_SIZE and pos_count < TEAM_STRUCTURE[pos]:
                team.players.append(player)
                break

    # Step 4: Return offspring as-is (even if overbudget)
    return FootballSolution(offspring_teams, players_df)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


def crossover_position_based(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Crossover que garante equipas com estrutura correta (1 GK, 2 DEF, 2 MID, 2 FWD),
    evitando jogadores duplicados entre equipas.
    """
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())
    offspring_teams = []
    used_names = set()  # <- GLOBAL agora

    print("\n[DEBUG] STEP 1: Structured position-wise selection")

    for team_idx in range(N_TEAMS):
        team_players = []

        # Agrupar por posição dos dois pais
        position_pool = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
        for parent in [p1, p2]:
            for p in parent.repr[team_idx].players:
                position_pool[p['Position']].append(p)

        # Selecionar jogadores por posição
        for pos, n_needed in expected_structure.items():
            pool = position_pool[pos]
            random.shuffle(pool)
            selected = []

            # Tentar obter do pool dos pais
            for p in pool:
                if p['Name'] not in used_names:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            # Se ainda faltar, completar com jogadores livres dessa posição
            if len(selected) < n_needed:
                available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                random.shuffle(available)
                for p in available:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            if len(selected) < n_needed:
                print(f"[❌ ERRO] Não foi possível preencher {n_needed} jogadores na posição {pos} para a equipa {team_idx+1}")
                raise SystemExit("Violação da estrutura mesmo após tentativa de preenchimento com jogadores livres.")

            team_players.extend(selected)

        offspring_teams.append(Team(team_players))
        print(f"Team {team_idx} created with {[p['Position'] for p in team_players]}")

    return FootballSolution(offspring_teams, players_df)


'''

✅ 1. Explicação completa do crossover_position_based passo a passo
O objetivo do crossover_position_based é criar um filho (solução) com 5 equipas, cada uma com:

7 jogadores

Estrutura exata de posições: 1 GK, 2 DEF, 2 MID, 2 FWD

Sem jogadores duplicados entre equipas

🔄 Etapas detalhadas:
Preparação

Agrupam-se todos os jogadores do dataset (players_df) num dicionário name_to_player.

É criado um conjunto used_names para rastrear os jogadores já usados em qualquer equipa do filho.

Iteração por equipa (5 vezes)

Para cada equipa (team_idx de 0 a 4), criamos team_players = [].

Pool de jogadores por posição

Criamos um dicionário position_pool com listas de jogadores de p1 e p2 da mesma equipa.

Ex: position_pool['DEF'] contém todos os defesas dessa equipa nos dois pais.

Seleção por posição Para cada posição (GK, DEF, MID, FWD) com o número de jogadores exigido:

Tentamos escolher jogadores do position_pool, que ainda não foram usados noutras equipas (used_names).

Se não houver suficientes, completamos com jogadores livres do dataset da mesma posição.

A cada seleção, adicionamos o nome ao used_names.

Erro se faltar jogadores

Se mesmo assim não conseguirmos completar os jogadores para uma posição, o programa falha com erro.

Equipa construída

Junta-se os jogadores selecionados num objeto Team, que é adicionado à lista offspring_teams.

Resultado final

O filho (FootballSolution) é devolvido com as 5 equipas completas, com estrutura válida e sem duplicações.


'''



def crossover_position_based_debug_budget(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    """
    Igual ao crossover_position_based, mas imprime o budget total de cada equipa
    e mostra exatamente como será penalizado no fitness.
    """
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())
    offspring_teams = []
    used_names = set()

    print("\n[DEBUG] STEP 1: Structured position-wise selection")

    for team_idx in range(N_TEAMS):
        team_players = []

        position_pool = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
        for parent in [p1, p2]:
            for p in parent.repr[team_idx].players:
                position_pool[p['Position']].append(p)

        for pos, n_needed in expected_structure.items():
            pool = position_pool[pos]
            random.shuffle(pool)
            selected = []

            for p in pool:
                if p['Name'] not in used_names:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            if len(selected) < n_needed:
                available = [name_to_player[n] for n in all_names - used_names if name_to_player[n]['Position'] == pos]
                random.shuffle(available)
                for p in available:
                    selected.append(p)
                    used_names.add(p['Name'])
                    if len(selected) == n_needed:
                        break

            if len(selected) < n_needed:
                print(f"[❌ ERRO] Não foi possível preencher {n_needed} jogadores na posição {pos} para a equipa {team_idx+1}")
                raise SystemExit("Violação da estrutura mesmo após tentativa de preenchimento com jogadores livres.")

            team_players.extend(selected)

        offspring_teams.append(Team(team_players))
        print(f"Team {team_idx} created with {[p['Position'] for p in team_players]}")

    # Criar solução final
    solution = FootballSolution(offspring_teams, players_df)

    # DEBUG EXTRA: calcular penalizações
    print("\n[DEBUG] Budget e Penalizações de Fitness:")
    penalty = 0
    for i, team in enumerate(solution.repr):
        total = team.total_salary()
        excess = total - MAX_BUDGET
        if excess > 0:
            print(f"  Equipa {i+1} → Budget: {total:.1f}M → Excede em {excess:.1f}M → Penalização: {excess * 0.5:.3f}")
            penalty += excess * 0.5
        else:
            print(f"  Equipa {i+1} → Budget: {total:.1f}M → OK")

    skills = [team.average_skill() for team in solution.repr]
    std = np.std(skills)
    base_score = 1 / (1 + std)
    final_fitness = max(0.001, base_score - penalty)

    print(f"\n[DEBUG] STD das skills: {std:.4f} → Base Score: {base_score:.4f}")
    print(f"[DEBUG] Penalização Total: {penalty:.4f}")
    print(f"[DEBUG] Fitness Final Estimado: {final_fitness:.4f}")

    return solution




def crossover_position_based_explained(p1: FootballSolution, p2: FootballSolution) -> FootballSolution:
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    name_to_player = {p['Name']: p for _, p in players_df.iterrows()}
    all_names = set(name_to_player.keys())
    offspring_teams = []
    used_names = set()

    print("\n===== [INÍCIO] Crossover baseado em posição =====")
    print("- Vamos criar 5 equipas, cada uma com 7 jogadores")
    print("- Estrutura: 1 GK, 2 DEF, 2 MID, 2 FWD")
    print("- Jogadores já usados serão guardados em used_names para evitar duplicações.")

    for team_idx in range(N_TEAMS):
        print(f"\n\n=== [EQUIPA {team_idx+1}] ===")
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
                print(f"[❌ ERRO] Não foi possível preencher {n_needed} jogadores da posição {pos}")
                raise SystemExit("Violação da estrutura mesmo após usar o dataset.")

            team_players.extend(selected)

        print(f"\n✅ Equipa {team_idx+1} criada com:")
        for p in team_players:
            print(f"  - {p['Name']} ({p['Position']})")

        offspring_teams.append(Team(team_players))
        print(f"🔒 used_names atualizado: {sorted(used_names)}")

    print("\n===== [FINAL] Solução construída com 5 equipas sem duplicados =====")
    print(f"Número total de jogadores únicos: {len(used_names)} (esperado: {N_TEAMS * TEAM_SIZE})")

    return FootballSolution(offspring_teams, players_df)




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------