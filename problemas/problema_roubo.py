from aima.search import Problem

class ProblemaRoubo(Problem):
    """
    Problema: Ladrão entra no banco, pega a joia e sai pelo ponto de entrada
    """
    
    def __init__(self, initial, goal, grid, posicoes_seguranca):
        """
        initial: (x_ladrao, y_ladrao, tem_joia, tempo)
        grid: matriz do banco (0 = livre, 1 = parede, 2 = joia)
        posicoes_seguranca: dicionário {tempo: (x_seg, y_seg)}
        """
        self.grid = grid
        self.posicoes_seguranca = posicoes_seguranca
        self.largura = len(grid[0])
        self.altura = len(grid)
        super().__init__(initial, goal)
    
    def actions(self, state):
        """Retorna ações possíveis dado o estado atual"""
        x, y, tem_joia, tempo = state
        actions = []
        
        pos_seg_prox = self.posicoes_seguranca.get(tempo + 1, None)
        
        movimentos = [
            ('cima', (x, y-1)),
            ('baixo', (x, y+1)),
            ('esquerda', (x-1, y)),
            ('direita', (x+1, y))
        ]
        
        for acao, (nx, ny) in movimentos:
            if 0 <= nx < self.largura and 0 <= ny < self.altura:
                if self.grid[ny][nx] != 1:
                    if pos_seg_prox is None or (nx, ny) != pos_seg_prox:
                        actions.append(acao)
        
        if not tem_joia and self.grid[y][x] == 2:
            actions.append('pegar_joia')
            
        return actions
    
    def result(self, state, action):
        """Retorna o novo estado após executar a ação"""
        x, y, tem_joia, tempo = state
        novo_tempo = tempo + 1
        
        if action == 'pegar_joia':
            return (x, y, True, novo_tempo)
        
        if action == 'cima':
            return (x, y-1, tem_joia, novo_tempo)
        elif action == 'baixo':
            return (x, y+1, tem_joia, novo_tempo)
        elif action == 'esquerda':
            return (x-1, y, tem_joia, novo_tempo)
        elif action == 'direita':
            return (x+1, y, tem_joia, novo_tempo)
        
        return (x, y, tem_joia, novo_tempo)
    
    def goal_test(self, state):
        """Objetivo: estar na entrada com a joia"""
        x, y, tem_joia, _ = state
        x_entrada, y_entrada = self.initial[0], self.initial[1]
        return (x, y) == (x_entrada, y_entrada) and tem_joia
    
    def path_cost(self, c, state1, action, state2):
        """Custo: tempo (cada ação custa 1)"""
        return c + 1