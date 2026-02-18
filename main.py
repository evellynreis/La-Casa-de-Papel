import time
from ambiente.banco_ambiente import BancoAmbiente
from ambiente.agente_seguranca import SegurancaAgente
from agentes.ladrao_agente import LadraoAgente

def criar_casa_da_moeda():
    """
    Cria o grid da Casa da Moeda da Espanha
    0: corredor, 1: parede, 2: joia, 5: entrada
    """
    grid = [
        [5, 0, 0, 0, 1, 0, 0, 0],  # Entrada na posição (0,0)
        [1, 1, 0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 2, 0, 0, 0, 0],  # Joia na posição (3,4)
        [1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 1, 0]
    ]
    return grid

def criar_trajetoria_arturito():
    """
    Cria a trajetória previsível do segurança Arturito
    Ele faz ronda em um padrão fixo de vai-e-vem
    """
    trajetoria = {}
    
    for t in range(50):
        if t < 15:  # Vai para a direita
            x = min(2 + t, 6)
            trajetoria[t] = (x, 2)
        elif t < 30:  # Volta para a esquerda
            x = max(6 - (t - 15), 2)
            trajetoria[t] = (x, 2)
        elif t < 40:  # Vai para a direita novamente
            x = min(2 + (t - 30), 6)
            trajetoria[t] = (x, 2)
        else:  # Volta para a esquerda
            x = max(6 - (t - 40), 2)
            trajetoria[t] = (x, 2)
    
    return trajetoria

def main():
    print("=" * 60)
    print("🏦 LA CASA DE PAPEL - O ROUBO À CASA DA MOEDA")
    print("=" * 60)
    print("\n🎬 SINOPSE:")
    print("O Professor (🧑) precisa infiltrar-se na Casa da Moeda,")
    print("roubar a joia (💎) e escapar pela entrada (🚪),")
    print("desviando do segurança Arturito (👮) que faz ronda.")
    print("\n📋 PRESSIONE ENTER PARA COMEÇAR...")
    input()
    
    # Configuração inicial
    grid = criar_casa_da_moeda()
    trajetoria = criar_trajetoria_arturito()
    
    # Cria ambiente
    ambiente = BancoAmbiente(grid, trajetoria)
    
    # Cria agentes
    ladrao = LadraoAgente(
        posicao_inicial=(0, 0),
        grid=grid,
        trajetoria_seguranca=trajetoria
    )
    
    seguranca = SegurancaAgente(
        posicao_inicial=trajetoria[0]
    )
    
    # Adiciona agentes ao ambiente
    ambiente.add_agent(ladrao)
    ambiente.add_agent(seguranca)
    
    # Loop principal do jogo
    passo = 0
    pos_ladrao = (0, 0)
    
    while ambiente.jogo_ativo and passo < 50:
        ambiente.passo_atual = passo
        ambiente.render()
        
        # Executa passo
        ambiente.step()
        
        # Verifica condições de vitória/derrota
        pos_ladrao = ambiente.get_posicao_ladrao()
        pos_seg = ambiente.get_posicao_seguranca()
        
        # Ladrão pego?
        if pos_ladrao == pos_seg:
            print("\n❌ ARTURITO PEGOU O PROFESSOR! FIM DE JOGO!")
            ambiente.jogo_ativo = False
            break
        
        # Ladrão venceu?
        if pos_ladrao == (0, 0) and ambiente.ladrao_joia:
            print("\n🏆 MISSÃO CUMPRIDA! O PROFESSOR ESCAPOU COM A JOIA!")
            print("🎉 LA CASA DE PAPEL - TEMPORADA 1: SUCESSO!")
            ambiente.jogo_ativo = False
            break
        
        passo += 1
        time.sleep(1)
    
    ambiente.render()
    print("\n📊 ESTATÍSTICAS FINAIS:")
    print(f"Passos totais: {passo}")
    print(f"Joia roubada: {'SIM ✅' if ambiente.ladrao_joia else 'NÃO ❌'}")
    print(f"Professor escapou: {'SIM 🏆' if (pos_ladrao == (0,0) and ambiente.ladrao_joia) else 'NÃO 💀'}")

if __name__ == "__main__":
    main()