from aima.search import astar_search
from problemas.problema_roubo import ProblemaRoubo
from problemas.heuristica import heuristica_com_seguranca

class ProgramaProfessor:
    """
    Programa de agente do Professor (ladrão)
    Usa A* para planejar a rota de fuga
    """
    
    def __init__(self, grid, trajetoria_seguranca):
        self.grid = grid
        self.trajetoria_seguranca = trajetoria_seguranca
        self.plano = []
        self.estado_atual = None
        
    def decidir_acao(self, percepcao):
        """
        Decide a próxima ação baseado na percepção atual
        """
        if not percepcao:
            return None
            
        posicao = percepcao.get('posicao', (0, 0))
        tem_joia = percepcao.get('tem_joia', False)
        tempo = percepcao.get('tempo', 0)
        
        self.estado_atual = (posicao[0], posicao[1], tem_joia, tempo)
        
        # Se não tem plano ou plano foi executado, replaneja
        if not self.plano:
            self.plano = self.planejar_rota(self.estado_atual)
            if self.plano:
                print(f"\n📋 NOVO PLANO GERADO: {self.plano}\n")
        
        # Pega próxima ação do plano
        if self.plano:
            return self.plano.pop(0)
        return None
    
    def planejar_rota(self, estado_atual):
        """
        Usa A* para planejar a melhor rota
        """
        def objetivo(state):
            x, y, tem_joia, _ = state
            x_entrada, y_entrada = estado_atual[0], estado_atual[1]
            return (x, y) == (x_entrada, y_entrada) and tem_joia
        
        problema = ProblemaRoubo(
            initial=estado_atual,
            goal=objetivo,
            grid=self.grid,
            posicoes_seguranca=self.trajetoria_seguranca
        )
        
        try:
            resultado = astar_search(
                problema, 
                h=lambda node: heuristica_com_seguranca(node.state, problema)
            )
            
            if resultado:
                caminho = resultado.path()
                acoes = [no.action for no in caminho[1:] if no.action]
                return acoes
        except Exception as e:
            print(f"Erro na busca: {e}")
            
        return []