from aima3.agents import Agent

class LadraoAgente(Agent):
    def __init__(self, posicao_inicial, programa):
        super().__init__(programa.decidir_acao)
        self.posicao = posicao_inicial
        self.programa_ladrao = programa 
        self.performance = 0