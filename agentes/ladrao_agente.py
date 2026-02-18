from aima3.agents import Agent
from agentes.programa_ladrao import ProgramaProfessor

class LadraoAgente(Agent):
    """
    Agente ladrão (Professor) - usa busca A* para planejar.
    O Agent do AIMA espera receber uma função 'program' no init.
    """
    
    def __init__(self, posicao_inicial, grid, trajetoria_seguranca):
        # Primeiro, instanciamos a lógica do programa
        self.programa_ladrao = ProgramaProfessor(grid, trajetoria_seguranca)
        
        # Passamos o método decidir_acao como o 'program' do Agente
        super().__init__(self.programa_ladrao.decidir_acao)
        
        # Atributos auxiliares de estado
        self.posicao = posicao_inicial
        self.performance = 0