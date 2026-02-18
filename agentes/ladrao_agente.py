from aima3.agents import Agent
from agentes.programa_ladrao import ProgramaProfessor

class LadraoAgente(Agent):
    """
    Agente ladrão (Professor) - usa busca A* para planejar.
    O Agent do AIMA espera receber uma função 'program' no init.
    """
    
class LadraoAgente(Agent):

    def __init__(self, posicao_inicial, programa):
        super().__init__(programa.decidir_acao)
        self.posicao = posicao_inicial
        self.performance = 0