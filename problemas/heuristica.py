def manhattan(p1, p2):
    """Calcula a distância de Manhattan entre dois pontos."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def encontrar_joia(grid):
    """Localiza a coordenada (x, y) do valor 2 no grid."""
    for y, linha in enumerate(grid):
        for x, valor in enumerate(linha):
            if valor == 2:
                return (x, y)
    return None

def heuristica_ladrao(state, problema):
    """
    Estima o custo restante. Se não tem a joia, o custo é:
    dist(atual -> joia) + dist(joia -> saída).
    """
    x, y, tem_joia, _ = state
    x_saida, y_saida = problema.initial[0], problema.initial[1]
    
    if not tem_joia:
        pos_joia = encontrar_joia(problema.grid)
        if not pos_joia: return 0
        
        dist_ate_joia = manhattan((x, y), pos_joia)
        dist_joia_ate_saida = manhattan(pos_joia, (x_saida, y_saida))
        return dist_ate_joia + dist_joia_ate_saida
    else:
        # Se já tem a joia, basta voltar para a saída
        return manhattan((x, y), (x_saida, y_saida))

def heuristica_com_seguranca(state, problema):
    """
    Adiciona uma penalidade à distância de Manhattan se o ladrão
    estiver em rota de colisão com o segurança.
    """
    x, y, tem_joia, tempo = state
    dist_base = heuristica_ladrao(state, problema)
    
    # Pega a posição do segurança prevista para este tempo
    pos_seg = problema.posicoes_seguranca.get(tempo, None)
    
    if pos_seg:
        dist_seg = manhattan((x, y), pos_seg)
        # Se estiver a menos de 3 blocos, aumenta o custo drasticamente
        if dist_seg < 3:
            return dist_base + (10 * (3 - dist_seg))
            
    return dist_base