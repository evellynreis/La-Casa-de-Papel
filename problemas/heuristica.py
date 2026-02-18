def heuristica_ladrao(state, problema):
    """
    Heurística base: distância de Manhattan até a joia + 
    distância da joia até a saída
    """
    x, y, tem_joia, tempo = state
    
    if not tem_joia:
        # Ainda precisa pegar a joia
        pos_joia = encontrar_joia(problema.grid)
        dist_joia = manhattan((x, y), pos_joia)
        dist_saida = manhattan(pos_joia, (problema.initial[0], problema.initial[1]))
        return dist_joia + dist_saida
    else:
        # Já tem a joia: distância até a saída
        return manhattan((x, y), (problema.initial[0], problema.initial[1]))

def heuristica_com_seguranca(state, problema):
    """
    Heurística avançada que considera a posição futura do segurança
    """
    x, y, tem_joia, tempo = state
    
    # Distância base
    dist_base = heuristica_ladrao(state, problema)
    
    # Verifica posição do segurança no tempo atual
    pos_seg = problema.posicoes_seguranca.get(tempo, (x, y))
    dist_seg = manhattan((x, y), pos_seg)
    
    # Penalidade se estiver perto do segurança
    if dist_seg < 3:
        penalidade = (3 - dist_seg) * 5
    else:
        penalidade = 0
    
    return dist_base + penalidade

def manhattan(p1, p2):
    """Distância de Manhattan entre dois pontos"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def encontrar_joia(grid):
    """Encontra a posição da joia no grid"""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 2:
                return (x, y)
    return (0, 0)