import pytest
from problemas.problema_roubo import ProblemaRoubo
from problemas.heuristica import heuristica_ladrao, heuristica_com_seguranca, manhattan
from aima.search import astar_search

def test_manhattan():
    """Testa a função de distância de Manhattan"""
    assert manhattan((0, 0), (3, 4)) == 7
    assert manhattan((1, 1), (1, 1)) == 0
    assert manhattan((5, 5), (2, 3)) == 5

def test_heuristica_admissivel():
    """Testa se heurística é admissível (não superestima)"""
    grid = [[5, 0, 0], [0, 1, 0], [0, 0, 2]]
    
    problema = ProblemaRoubo(
        initial=(0, 0, False, 0),
        goal=lambda s: False,
        grid=grid,
        posicoes_seguranca={}
    )
    
    state = (0, 0, False, 0)
    h = heuristica_ladrao(state, problema)
    
    # Distância real mínima: até joia (2,2) + joia até saída (0,0)
    # Manhattan real: 4 + 4 = 8
    assert h <= 8

def test_astar_encontra_solucao():
    """Testa se A* encontra solução para um problema simples"""
    grid = [[5, 0, 0], [0, 1, 0], [0, 0, 2]]
    trajetoria = {}
    
    problema = ProblemaRoubo(
        initial=(0, 0, False, 0),
        goal=lambda s: s[0] == 0 and s[1] == 0 and s[2] == True,
        grid=grid,
        posicoes_seguranca=trajetoria
    )
    
    resultado = astar_search(problema, h=lambda n: heuristica_ladrao(n.state, problema))
    assert resultado is not None
    assert resultado.state[2] == True  # Tem a joia

if __name__ == "__main__":
    pytest.main([__file__])