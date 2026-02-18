from aima.agents import Environment, Agent
import time
import os

class BancoAmbiente(Environment):
    """
    Ambiente da Casa da Moeda (grid)
    0 = corredor livre
    1 = parede
    2 = joia
    3 = ladrão
    4 = segurança
    5 = entrada/saída
    """
    
    def __init__(self, grid, trajetoria_seguranca):
        super().__init__()
        self.grid = [linha[:] for linha in grid]
        self.grid_original = grid
        self.trajetoria_seguranca = trajetoria_seguranca
        self.passo_atual = 0
        self.ladrao_joia = False
        self.jogo_ativo = True
        self.agents = []
        
    def percept(self, agent):
        """Retorna a percepção para um agente"""
        from agentes.ladrao_agente import LadraoAgente
        from ambiente.agente_seguranca import SegurancaAgente
        
        if isinstance(agent, LadraoAgente):
            return {
                'posicao': agent.posicao,
                'tem_joia': self.ladrao_joia,
                'tempo': self.passo_atual,
                'pos_seguranca': self.get_posicao_seguranca(),
                'grid_vizinhanca': self.get_vizinhanca(agent.posicao, 3)
            }
        elif isinstance(agent, SegurancaAgente):
            return {
                'posicao': agent.posicao,
                'tempo': self.passo_atual,
                'pos_ladrao': self.get_posicao_ladrao()
            }
        return {}
    
    def execute_action(self, agent, action):
        """Executa a ação de um agente no ambiente"""
        from agentes.ladrao_agente import LadraoAgente
        
        if isinstance(agent, LadraoAgente):
            self.executar_acao_ladrao(agent, action)
        else:
            self.executar_acao_seguranca(agent, action)
    
    def executar_acao_ladrao(self, agente, acao):
        """Executa ação do ladrão"""
        x, y = agente.posicao
        
        if acao == 'pegar_joia' and self.grid[y][x] == 2:
            self.ladrao_joia = True
            self.grid[y][x] = 0
            print("🔑 LADRÃO PEGOU A JOIA!")
            
        elif acao in ['cima', 'baixo', 'esquerda', 'direita']:
            novo_x, novo_y = self.calcular_nova_posicao((x, y), acao)
            
            if 0 <= novo_x < len(self.grid[0]) and 0 <= novo_y < len(self.grid):
                if self.grid[novo_y][novo_x] != 1:
                    pos_seg = self.get_posicao_seguranca()
                    if (novo_x, novo_y) != pos_seg:
                        self.grid[y][x] = self.grid_original[y][x]
                        agente.posicao = (novo_x, novo_y)
                        self.grid[novo_y][novo_x] = 3
                    
    def executar_acao_seguranca(self, agente, acao):
        """Segue trajetória predefinida"""
        if self.passo_atual < len(self.trajetoria_seguranca):
            x_ant, y_ant = agente.posicao
            nova_pos = self.trajetoria_seguranca.get(self.passo_atual, agente.posicao)
            
            self.grid[y_ant][x_ant] = self.grid_original[y_ant][x_ant]
            agente.posicao = nova_pos
            x, y = nova_pos
            if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                self.grid[y][x] = 4
    
    def render(self):
        """Renderiza o estado atual do ambiente"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 50)
        print(f"🏦 CASA DA MOEDA DA ESPANHA - PASSO {self.passo_atual}")
        print("=" * 50)
        
        # Legenda
        print("🧑 Professor (Ladrão) | 👮 Arturito (Segurança) | 💎 Joia | 🚪 Entrada")
        print()
        
        for y in range(len(self.grid)):
            linha = ""
            for x in range(len(self.grid[0])):
                if (x, y) == self.get_posicao_ladrao():
                    linha += "🧑 "
                elif (x, y) == self.get_posicao_seguranca():
                    linha += "👮 "
                elif (x, y) == (0, 0):
                    linha += "🚪 "
                elif self.grid[y][x] == 2:
                    linha += "💎 "
                elif self.grid[y][x] == 1:
                    linha += "🧱 "
                else:
                    linha += "⬜ "
            print(linha)
        
        print()
        print(f"Joia com ladrão: {'SIM ✅' if self.ladrao_joia else 'NÃO ❌'}")
        print(f"Status: {'JOGO ATIVO' if self.jogo_ativo else 'FIM DE JOGO'}")
        print("=" * 50)
    
    def step(self):
        """Executa um passo no ambiente"""
        if self.jogo_ativo:
            for agent in self.agents[:]:
                percept = self.percept(agent)
                action = agent.program(percept)
                if action:
                    self.execute_action(agent, action)
            self.passo_atual += 1
    
    def add_agent(self, agent):
        """Adiciona um agente ao ambiente"""
        self.agents.append(agent)
    
    def get_posicao_seguranca(self):
        """Retorna posição atual do segurança"""
        from ambiente.agente_seguranca import SegurancaAgente
        for agent in self.agents:
            if isinstance(agent, SegurancaAgente):
                return agent.posicao
        return (0, 0)
    
    def get_posicao_ladrao(self):
        """Retorna posição atual do ladrão"""
        from agentes.ladrao_agente import LadraoAgente
        for agent in self.agents:
            if isinstance(agent, LadraoAgente):
                return agent.posicao
        return (0, 0)
    
    def get_vizinhanca(self, pos, raio):
        """Retorna a vizinhança ao redor de uma posição"""
        x, y = pos
        vizinhanca = []
        for dy in range(-raio, raio+1):
            linha = []
            for dx in range(-raio, raio+1):
                nx, ny = x+dx, y+dy
                if 0 <= nx < len(self.grid[0]) and 0 <= ny < len(self.grid):
                    linha.append(self.grid[ny][nx])
                else:
                    linha.append(1)
            vizinhanca.append(linha)
        return vizinhanca
    
    def calcular_nova_posicao(self, pos, acao):
        x, y = pos
        if acao == 'cima':
            return (x, y-1)
        elif acao == 'baixo':
            return (x, y+1)
        elif acao == 'esquerda':
            return (x-1, y)
        elif acao == 'direita':
            return (x+1, y)
        return pos