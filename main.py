import collections
import collections.abc

# Patch para compatibilidade com Python 3.10+
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

import time
from ambiente.banco_ambiente import BancoAmbiente
from ambiente.agente_seguranca import SegurancaAgente
from agentes.ladrao_agente import LadraoAgente

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

def criar_trajetoria_arturito():
    trajetoria = {}
    for t in range(100): # Aumentado para cobrir mais passos
        if (t // 15) % 2 == 0: # Vai e volta a cada 15 passos
            x = min(2 + (t % 15), 6)
        else:
            x = max(6 - (t % 15), 2)
        trajetoria[t] = (x, 2)
    return trajetoria

def main():
    print("=" * 60)
    print("🏦 LA CASA DE PAPEL - O ROUBO À CASA DA MOEDA")
    print("=" * 60)
    
    grid = criar_casa_da_moeda()
    trajetoria = criar_trajetoria_arturito()
    
    ambiente = BancoAmbiente(grid, trajetoria)
    
    # IMPORTANTE: Passar a trajetória para o segurança
    ladrao = LadraoAgente(posicao_inicial=(0, 0), grid=grid, trajetoria_seguranca=trajetoria)
    seguranca = SegurancaAgente(posicao_inicial=(2, 2), trajetoria=trajetoria)
    
    ambiente.add_thing(ladrao)
    ambiente.add_thing(seguranca)
    
    passo = 0
    while ambiente.jogo_ativo and passo < 60:
        ambiente.step() # O step já chama o render que corrigimos antes
        
        pos_ladrao = ambiente.get_posicao_agente('LadraoAgente')
        pos_seg = ambiente.get_posicao_agente('SegurancaAgente')
        
        if pos_ladrao == pos_seg:
            print("\n🚨 PERIGO! O PROFESSOR FOI PEGO POR ARTURITO!")
            break
            
        if pos_ladrao == (0, 0) and ambiente.ladrao_joia and passo > 1:
            print("\n🏆 SUCESSO! O PROFESSOR ESCAPOU COM A JOIA!")
            break
            
        passo += 1
        time.sleep(0.4)

if __name__ == "__main__":
    main()