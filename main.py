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
    trajetoria = {}

    for t in range(100):
        if (t // 15) % 2 == 0:
            x = min(2 + (t % 15), 6)
        else:
            x = max(6 - (t % 15), 2)

        trajetoria[t] = (x, 2)

    return trajetoria


def main():
    print("=" * 60)
    print("🏦 LA CASA DE PAPEL - O ROUBO À CASA DA MOEDA")
    print("=" * 60)

    print("\nEscolha o modo de jogo:")
    print("1 - 🤖 IA (A* automático)")
    print("2 - 🎮 Jogar manualmente")

    modo = input("\nDigite sua opção: ").strip()

    grid = criar_casa_da_moeda()
    trajetoria = criar_trajetoria_policia()

    ambiente = BancoAmbiente(grid, trajetoria)

    # Escolha do programa do ladrão
    if modo == '1':
        print("\n🤖 Modo IA ativado!")
        programa = ProgramaProfessor(grid, trajetoria)
    else:
        print("\n🎮 Modo Manual ativado!")
        programa = ProgramaHumano()

    ladrao = LadraoAgente(
        posicao_inicial=(0, 0),
        programa=programa
    )

    policia = PoliciaAgente(
        posicao_inicial=(2, 2),
        trajetoria=trajetoria
    )

    ambiente.add_thing(ladrao)
    ambiente.add_thing(policia)

    passo = 0

    while ambiente.jogo_ativo and passo < 60:

        ambiente.step()

        pos_ladrao = ambiente.get_posicao_agente('LadraoAgente')
        pos_policia = ambiente.get_posicao_agente('PoliciaAgente')

        # Se colidiu com o segurança
        if pos_ladrao == pos_policia:
            print("\n🚨 PERIGO! O PROFESSOR FOI PEGO PELA POLÍCIA!")
            break

        # Se voltou para saída com a joia
        if pos_ladrao == (0, 0) and ambiente.ladrao_joia and passo > 1:
            print("\n🏆 SUCESSO! O PROFESSOR ESCAPOU COM A JOIA!")
            break

        passo += 1

        # Sleep apenas no modo IA
        if modo == '1':
            time.sleep(0.4)

    print("\n🏁 FIM DE JOGO")
    print("=" * 60)


if __name__ == "__main__":
    main()