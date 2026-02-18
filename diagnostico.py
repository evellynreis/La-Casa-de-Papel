import os
import sys

def preparar_ambiente():
    print("🛠 Preparando estrutura de pastas...")
    pastas = ['agentes', 'ambiente', 'problemas', 'tests']
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
        
        init_file = os.path.join(pasta, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f"# Pacote {pasta}\n")
            print(f"✅ Criado: {init_file}")

    try:
        import aima
        print("✅ Biblioteca AIMA detectada.")
    except ImportError:
        print("❌ AIMA não encontrada. Execute: pip install aima-python")

if __name__ == "__main__":
    preparar_ambiente()