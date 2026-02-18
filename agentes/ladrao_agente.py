from aima.agents import Agent
from agentes.programa_ladrao import ProgramaProfessor

class LadraoAgente(Agent):
    """Agente ladrão (Professor) - usa busca A* para planejar"""
    
    def __init__(self, posicao_inicial, grid, trajetoria_seguranca):
        self.programa_ladrao = ProgramaProfessor(grid, trajetoria_seguranca)
        super().__init__(self.programa_ladrao.decidir_acao)
        self.posicao = posicao_inicial
        self.plano_atual = []