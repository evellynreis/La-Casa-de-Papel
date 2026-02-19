class ProgramaHumano:
    """
    Programa de agente controlado pelo usuário.
    """

    def decidir_acao(self, percepcao):
        print("\n🎮 Controle o Professor:")
        print("W = cima | S = baixo | A = esquerda | D = direita")

        comando = input("Sua ação: ").lower()

        mapa = {
            'w': 'cima',
            's': 'baixo',
            'a': 'esquerda',
            'd': 'direita',
            'p': 'pegar_joia'
        }

        return mapa.get(comando, 'NoOp')
