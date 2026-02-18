from aima3.search import astar_search
from problemas.problema_roubo import ProblemaRoubo
from problemas.heuristica import heuristica_com_seguranca

class ProgramaProfessor:
    """
    Programa de agente do Professor (ladrão).
    Gerencia o ciclo de percepção -> planejamento -> ação.
    """
    
    def __init__(self, grid, trajetoria_seguranca):
        self.grid = grid
        self.trajetoria_seguranca = trajetoria_seguranca
        self.plano = []
        self.tentou_planejar = False # Evita recalculação infinita em caso de erro
        
    def decidir_acao(self, percepcao):
        """
        Decide a próxima ação baseado na percepção atual (dicionário).
        """
        if not percepcao:
            return 'NoOp'
            
        posicao = percepcao.get('posicao', (0, 0))
        tem_joia = percepcao.get('tem_joia', False)
        tempo = percepcao.get('tempo', 0)
        
        estado_atual = (posicao[0], posicao[1], tem_joia, tempo)
        
        # Se não há plano e ainda não falhamos em planejar, busca a rota
        if not self.plano and not self.tentou_planejar:
            self.plano = self.planejar_rota(estado_atual)
            self.tentou_planejar = True # Marca que já houve uma tentativa de plano
            
            if self.plano:
                print(f"\n📋 NOVO PLANO GERADO ({len(self.plano)} passos)\n")
            else:
                print("\n⚠️ FALHA AO GERAR PLANO: Caminho impossível ou sem solução.\n")
        
        # Executa o plano passo a passo
        if self.plano:
            return self.plano.pop(0)
            
        return 'NoOp' # 'NoOp' é a ação padrão do AIMA para "fazer nada"
    
    def planejar_rota(self, estado_inicial):
        """
        Usa A* para planejar a melhor rota considerando a segurança.
        """
        # Define a função objetivo: estar na posição de entrada COM a joia
        def teste_objetivo(state):
            x, y, tem_joia, _ = state
            # O objetivo é retornar à posição inicial do plano (entrada) com a joia
            return (x, y) == (estado_inicial[0], estado_inicial[1]) and tem_joia
        
        problema = ProblemaRoubo(
            initial=estado_inicial,
            goal=teste_objetivo,
            grid=self.grid,
            posicoes_seguranca=self.trajetoria_seguranca
        )
        
        try:
            # Executa a busca A* com a heurística fornecida
            resultado = astar_search(
                problema, 
                h=lambda node: heuristica_com_seguranca(node.state, problema)
            )
            
            if resultado:
                # Converte o nó resultado em uma lista de ações
                # O caminho inclui o nó raiz (estado atual), por isso pegamos de [1:]
                acoes = [no.action for no in resultado.path() if no.action]
                return acoes
        except Exception as e:
            print(f"Erro crítico na busca A*: {e}")
            
        return []