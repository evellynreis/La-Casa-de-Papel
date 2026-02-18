from aima3.agents import Environment
import os

class BancoAmbiente(Environment):
    """
    Ambiente da Casa da Moeda (grid)
    """
    
    def __init__(self, grid, trajetoria_seguranca):
        super().__init__()
        self.grid = [linha[:] for linha in grid]
        self.grid_original = [linha[:] for linha in grid]
        self.trajetoria_seguranca = trajetoria_seguranca
        self.passo_atual = 0
        self.ladrao_joia = False
        self.jogo_ativo = True

    def add_thing(self, thing, location=None):
        """
        Sobrescreve o método padrão para registrar agentes e atualizar o grid.
        """
        # No AIMA3, agentes são armazenados na lista self.agents
        # e outras coisas na lista self.things
        super().add_thing(thing, location)
        
        # Sincroniza a posição inicial do agente no grid visual
        if hasattr(thing, 'posicao'):
            x, y = thing.posicao
            # 3 para Ladrão, 4 para Segurança (conforme sua lógica de render)
            tipo = 3 if hasattr(thing, 'programa_ladrao') else 4
            self.grid[y][x] = tipo

    def percept(self, agent):
        """Retorna a percepção para um agente"""
        is_ladrao = hasattr(agent, 'programa_ladrao')
        
        percepcao = {
            'posicao': agent.posicao,
            'tempo': self.passo_atual,
        }
        
        if is_ladrao:
            percepcao.update({
                'tem_joia': self.ladrao_joia,
                'pos_seguranca': self.get_posicao_agente('PoliciaAgente'),
                'grid_vizinhanca': self.get_vizinhanca(agent.posicao, 3)
            })
        else:
            percepcao.update({
                'pos_ladrao': self.get_posicao_agente('LadraoAgente')
            })
            
        return percepcao
    
    def execute_action(self, agent, action):
        """Executa a ação baseada no tipo de agente"""
        if action == 'NoOp' or action is None:
            return

        is_ladrao = hasattr(agent, 'programa_ladrao')
        
        if is_ladrao:
            self.executar_acao_ladrao(agent, action)
        else:
            self.executar_acao_seguranca(agent, action)
    
    def executar_acao_ladrao(self, agente, acao):
        x, y = agente.posicao
        
        if acao == 'pegar_joia' and self.grid[y][x] == 2:
            self.ladrao_joia = True
            self.grid[y][x] = 0

            print("\n💎 PROFESSOR PEGOU A JOIA!")
            print("=" * 40)

            
        elif acao in ['cima', 'baixo', 'esquerda', 'direita']:
            novo_x, novo_y = self.calcular_nova_posicao((x, y), acao)
            
            if 0 <= novo_x < len(self.grid[0]) and 0 <= novo_y < len(self.grid):
                if self.grid[novo_y][novo_x] != 1:
                    if (novo_x, novo_y) != self.get_posicao_agente('PoliciaAgente'):
                        # Limpa posição anterior no grid visual
                        self.grid[y][x] = self.grid_original[y][x] if self.grid_original[y][x] != 2 else 0
                        agente.posicao = (novo_x, novo_y)
                        self.grid[novo_y][novo_x] = 3
                    
    def executar_acao_seguranca(self, agente, nova_pos):

        # Se por algum motivo não for tupla válida, ignora
        if not isinstance(nova_pos, tuple) or len(nova_pos) != 2:
            return

        x_ant, y_ant = agente.posicao
        agente.posicao = nova_pos

        if self.grid[y_ant][x_ant] == 4:
            self.grid[y_ant][x_ant] = self.grid_original[y_ant][x_ant]

        nx, ny = nova_pos

        if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
            self.grid[ny][nx] = 4

    def step(self):
        if self.jogo_ativo:
            super().step()
            self.passo_atual += 1
            self.render()

    def get_posicao_agente(self, tipo_nome):
        for agent in self.agents:
            if type(agent).__name__ == tipo_nome:
                return agent.posicao
        return (-1, -1)

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"🏦 PASSO: {self.passo_atual} | Joia: {'✅' if self.ladrao_joia else '❌'}")
        
        for y, linha_grid in enumerate(self.grid):
            display = ""
            for x, valor in enumerate(linha_grid):
                pos = (x, y)
                if pos == self.get_posicao_agente('LadraoAgente'):
                    display += "🧑 "
                elif pos == self.get_posicao_agente('PoliciaAgente'):
                    display += "👮 "
                elif valor == 1: display += "🧱 "
                elif valor == 2: display += "💎 "
                elif valor == 5: display += "🚪 "
                else: display += "⬜ "
            print(display)
        print("=" * 30)

    def get_vizinhanca(self, pos, raio):
        x, y = pos
        return [[self.grid[ny][nx] if (0<=nx<len(self.grid[0]) and 0<=ny<len(self.grid)) else 1 
                for nx in range(x-raio, x+raio+1)] 
                for ny in range(y-raio, y+raio+1)]

    def calcular_nova_posicao(self, pos, acao):
        x, y = pos
        movimentos = {'cima': (0, -1), 'baixo': (0, 1), 'esquerda': (-1, 0), 'direita': (1, 0)}
        dx, dy = movimentos.get(acao, (0, 0))
        return (x + dx, y + dy)