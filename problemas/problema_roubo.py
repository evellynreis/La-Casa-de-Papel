from aima3.search import Problem

class ProblemaRoubo(Problem):
    """
    Define o espaço de estados para o roubo: (x, y, tem_joia, tempo).
    O objetivo é coletar a joia e retornar ao ponto de partida.
    """
    
    def __init__(self, initial, goal, grid, posicoes_seguranca):
        super().__init__(initial, goal)
        self.grid = grid
        self.posicoes_seguranca = posicoes_seguranca
        self.largura = len(grid[0])
        self.altura = len(grid)
    
    def actions(self, state):
        """Retorna ações que não colidem com paredes ou com o segurança no próximo tempo."""
        x, y, tem_joia, tempo = state
        actions = []
        
        # O ladrão prevê onde o segurança estará no tempo t+1
        pos_seg_prox = self.posicoes_seguranca.get(tempo + 1, None)
        
        movimentos = [
            ('cima', (x, y-1)),
            ('baixo', (x, y+1)),
            ('esquerda', (x-1, y)),
            ('direita', (x+1, y))
        ]
        
        for acao, (nx, ny) in movimentos:
            if 0 <= nx < self.largura and 0 <= ny < self.altura:
                if self.grid[ny][nx] != 1: # Não é parede
                    # Só move se a próxima posição não for a mesma do segurança
                    if pos_seg_prox is None or (nx, ny) != pos_seg_prox:
                        actions.append(acao)
        
        # Ação especial para coletar o item
        if not tem_joia and self.grid[y][x] == 2:
            actions.append('pegar_joia')
            
        return actions
    
    def result(self, state, action):
        """Aplica a ação e incrementa o contador de tempo."""
        x, y, tem_joia, tempo = state
        novo_tempo = tempo + 1
        
        if action == 'pegar_joia':
            return (x, y, True, novo_tempo)
        
        # Mapeamento de movimentos
        mudancas = {
            'cima': (x, y-1),
            'baixo': (x, y+1),
            'esquerda': (x-1, y),
            'direita': (x+1, y)
        }
        
        nx, ny = mudancas.get(action, (x, y))
        return (nx, ny, tem_joia, novo_tempo)
    
    def goal_test(self, state):
        """
        Verifica se o estado atual satisfaz o objetivo.
        Se self.goal for uma função (como definido no programa_ladrao), usa ela.
        """
        if callable(self.goal):
            return self.goal(state)
            
        x, y, tem_joia, _ = state
        x_origem, y_origem = self.initial[0], self.initial[1]
        return (x, y) == (x_origem, y_origem) and tem_joia

    def path_cost(self, c, state1, action, state2):
        """Cada movimento ou ação custa 1 unidade de tempo."""
        return c + 1