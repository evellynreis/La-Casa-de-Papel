import pytest
from problemas.problema_roubo import ProblemaRoubo
from problemas.heuristica import heuristica_ladrao, manhattan
from aima3.search import astar_search

"""
Testa se a heurística não superestima o custo real
"""

def test_manhattan():
    assert manhattan((0, 0), (3, 4)) == 7
    assert manhattan((5, 5), (2, 3)) == 5

def test_heuristica_admissivel():
    grid = [[5, 0], [0, 2]] # Saída em (0,0), Joia em (1,1)
    # Distância mínima: (0,0)->(1,1) = 2 + (1,1)->(0,0) = 2. Total = 4.
    
    problema = ProblemaRoubo(initial=(0, 0, False, 0), goal=None, grid=grid, posicoes_seguranca={})
    h = heuristica_ladrao((0, 0, False, 0), problema)
    assert h <= 4

def test_astar_caminho_simples():
    grid = [[5, 0, 2]] # Linha reta: Entrada(0,0), Corredor(1,0), Joia(2,0)
    problema = ProblemaRoubo(
        initial=(0, 0, False, 0),
        goal=lambda s: s[0] == 0 and s[1] == 0 and s[2] == True,
        grid=grid,
        posicoes_seguranca={}
    )
    
    resultado = astar_search(problema, h=lambda n: heuristica_ladrao(n.state, problema))
    assert resultado is not None
    # O caminho deve ter: Direita, Direita, Pegar_Joia, Esquerda, Esquerda
    assert len(resultado.path()) > 4