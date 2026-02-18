from aima.agents import Agent

class SegurancaAgente(Agent):
    """Agente segurança (Arturito) - segue trajetória previsível"""
    
    def __init__(self, posicao_inicial):
        super().__init__(self.programa_seguranca)
        self.posicao = posicao_inicial
        self.trajetoria_idx = 0
        
    def programa_seguranca(self, percepcao):
        """
        Programa do segurança: segue padrão previsível
        O movimento é controlado pelo ambiente
        """
        return None