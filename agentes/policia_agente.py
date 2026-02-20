from aima3.agents import Agent

class PoliciaAgente(Agent):

    """Agente polícia - segue trajetória previsível"""
    
    def __init__(self, posicao_inicial, trajetoria):
        # O programa do agente apenas retorna a posição que ele deve estar
        super().__init__(self.programa_seguranca)
        self.posicao = posicao_inicial
        self.trajetoria = trajetoria # Dicionário {tempo: (x, y)}
        
    def programa_seguranca(self, percepcao):
        """
        A polícia não 'decide', ele segue o plano.
        Retorna a próxima posição baseada no tempo atual.
        """
        tempo_atual = percepcao.get('tempo', 0)
        proxima_pos = self.trajetoria.get(tempo_atual, self.posicao)
        return proxima_pos