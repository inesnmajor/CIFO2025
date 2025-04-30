from collections import Counter

def print_solution(label, solution):
    print(f"\n========== {label} ==========")
    for i, team in enumerate(solution.repr):
        print(f"\nEquipa {i+1}:")
        for player in team.players:
            print(f"  - {player['Name']} ({player['Position']}), Skill: {player['Skill']}, Salário: {player['Salary (€M)']}M")
    print("====================================\n")

def check_no_duplicates(solution):
    all_players = []
    for team in solution.repr:
        for player in team.players:
            all_players.append(player["Name"])
    counts = Counter(all_players)
    duplicates = [name for name, count in counts.items() if count > 1]
    if duplicates:
        print(f"[❌ Violação] Jogadores duplicados encontrados: {duplicates}")
        print_solution("Estado do indivíduo com duplicados", solution)
        raise SystemExit("Execução terminada devido a violação de duplicados.")
    return True

def check_team_size(solution, expected_size=7):
    for i, team in enumerate(solution.repr):
        if len(team.players) != expected_size:
            print(f"[❌ Violação] Equipa {i+1} tem {len(team.players)} jogadores (esperado: {expected_size})")
            print_solution(f"Estado da Equipa {i+1}", solution)
            raise SystemExit("Execução terminada devido a violação do tamanho da equipa.")
    return True

def check_budget(solution, max_budget=750):
    for i, team in enumerate(solution.repr):
        total_salary = sum(player["Salary (€M)"] for player in team.players)
        if total_salary > max_budget:
            print(f"[❌ Violação] Equipa {i+1} excede orçamento ({total_salary}M > {max_budget}M)")
            print_solution(f"Estado da Equipa {i+1}", solution)
            raise SystemExit("Execução terminada devido a violação do orçamento.")
    return True

def check_team_structure(solution):
    expected_structure = {'GK': 1, 'DEF': 2, 'MID': 2, 'FWD': 2}
    for i, team in enumerate(solution.repr):
        position_counts = Counter(player['Position'] for player in team.players)
        for pos, expected_count in expected_structure.items():
            actual_count = position_counts.get(pos, 0)
            if actual_count != expected_count:
                print(f"[❌ Violação] Equipa {i+1} tem {actual_count} jogadores na posição {pos} (esperado: {expected_count})")
                print_solution(f"Estado da Equipa {i+1}", solution)
                raise SystemExit("Execução terminada devido a violação da estrutura da equipa.")
    return True





def is_valid_solution(solution):
    try:
        check_no_duplicates(solution)
        check_team_size(solution)
        check_budget(solution)
        return True
    except SystemExit:
        return False
