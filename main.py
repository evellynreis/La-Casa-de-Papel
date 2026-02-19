import collections
import collections.abc

# Patch para compatibilidade com Python 3.10+
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

import time

from ambiente.banco_ambiente import BancoAmbiente
from ambiente.agente_seguranca import PoliciaAgente
from agentes.ladrao_agente import LadraoAgente
from agentes.programa_ladrao import ProgramaProfessor
from agentes.programa_humano import ProgramaHumano


def criar_casa_da_moeda():
    grid = [
        [5, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 2, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 0]
    ]
    return grid


def criar_trajetoria_policia():
    """
    Cria uma rota de patrulha complexa que dá a volta no banco.
    """
    rota = [
        (2, 2), (1, 2), (0, 2),                   
        (0, 3), (0, 4),                           
        (1, 4), (2, 4),                           
        (2, 5), (2, 6),                           
        (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),   
        (7, 5), (7, 4), (7, 3), (7, 2), (7, 1), (7, 0), 
        (6, 0), (5, 0),                           
        (5, 1), (5, 2),                           
        (4, 2), (3, 2)                            
    ]
    
    trajetoria = {}

    for t in range(100):
        posicao_atual = rota[t % len(rota)]
        trajetoria[t] = posicao_atual
        
    return trajetoria


def main():
    while True:
        print("=" * 60)
        print("🏦 LA CASA DE PAPEL - O ROUBO À CASA DA MOEDA")
        print("=" * 60)

        print("\nEscolha o modo de jogo:")
        print("1 - 🤖 IA (A* automático)")
        print("2 - 🎮 Jogar manualmente")
        print("0 - ❌ Sair")

        modo = input("\nDigite sua opção: ").strip()

        if modo == '0':
            print("\n👋 Saindo do jogo. Até a próxima!")
            break

        if modo not in ['1', '2']:
            print("\n⚠️ Opção inválida! Tente novamente.")
            continue

        grid = criar_casa_da_moeda()
        trajetoria = criar_trajetoria_policia()
        ambiente = BancoAmbiente(grid, trajetoria)

        if modo == '1':
            print("\n🤖 Modo IA ativado!")
            programa = ProgramaProfessor(grid, trajetoria)
        else:
            print("\n🎮 Modo Manual ativado!")
            programa = ProgramaHumano()

        ladrao = LadraoAgente(posicao_inicial=(0, 0), programa=programa)
        policia = PoliciaAgente(posicao_inicial=(2, 2), trajetoria=trajetoria)

        ambiente.add_thing(ladrao)
        ambiente.add_thing(policia)

        passo = 0
        while ambiente.jogo_ativo and passo < 100:
            ambiente.passo_atual = passo 
            ambiente.render()

            # 1. VEZ DO PROFESSOR
            percepcao_ladrao = ambiente.percept(ladrao)
            acao_ladrao = ladrao.program(percepcao_ladrao)
            ambiente.execute_action(ladrao, acao_ladrao)

            pos_ladrao = ambiente.get_posicao_agente('LadraoAgente')
            pos_policia = ambiente.get_posicao_agente('PoliciaAgente')

            # Checagem de Colisão 1: O Professor esbarrou na Polícia?
            if pos_ladrao == pos_policia:
                ambiente.render()
                print("\n🚨 PERIGO! O PROFESSOR ESBARROU NA POLÍCIA!")
                break

            # Checagem de Vitória
            if pos_ladrao == (0, 0) and ambiente.ladrao_joia:
                ambiente.render()
                print("\n🏆 SUCESSO! O PROFESSOR ESCAPOU COM A JOIA!")
                break

            # 2. VEZ DO POLICIAL
            percepcao_policia = ambiente.percept(policia)
            acao_policia = policia.program(percepcao_policia)
            ambiente.execute_action(policia, acao_policia)

            # Atualiza as posições pois o policial andou
            pos_ladrao = ambiente.get_posicao_agente('LadraoAgente')
            pos_policia = ambiente.get_posicao_agente('PoliciaAgente')

            # Checagem de Colisão 2: A Polícia pegou o Professor?
            if pos_ladrao == pos_policia:
                ambiente.render()
                print("\n🚨 PERIGO! O PROFESSOR FOI PEGO PELA POLÍCIA!")
                break

            passo += 1
            if modo == '1':
                time.sleep(0.4)

        print("\n🏁 FIM DE PARTIDA")
        
        jogar_novamente = input("\n🔄 Deseja jogar novamente? (s/n): ").lower().strip()
        if jogar_novamente != 's':
            print("\nObrigado por jogar! Até logo.")
            break


if __name__ == "__main__":
    main()