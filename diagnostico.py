# diagnostico.py
import sys
import subprocess
import os

def diagnostico():
    print("🔍 DIAGNÓSTICO DO PROJETO LA CASA DE PAPEL")
    print("=" * 60)
    
    # Diretório atual
    print(f"\n📌 Diretório atual: {os.getcwd()}")
    
    # Python
    print(f"\n📌 Python: {sys.version}")
    print(f"📌 Executable: {sys.executable}")
    
    # Verifica arquivos __init__.py
    print("\n📌 Verificando arquivos __init__.py:")
    dirs_para_verificar = ['ambiente', 'agentes', 'problemas', 'tests']
    for dir_name in dirs_para_verificar:
        init_path = os.path.join(dir_name, '__init__.py')
        if os.path.exists(init_path):
            print(f"   ✅ {init_path}")
        else:
            print(f"   ❌ {init_path} - CRIE ESTE ARQUIVO!")
            # Cria o arquivo se não existir
            with open(init_path, 'w') as f:
                f.write('# Arquivo de inicialização do pacote\n')
            print(f"      ✓ Arquivo criado!")
    
    # Verifica pacotes instalados
    print("\n📌 Pacotes instalados:")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if 'aima' in line or 'pytest' in line:
                print(f"   📦 {line}")
    except:
        print("   ❌ Não foi possível listar pacotes")
    
    # Testa import do aima
    print("\n📌 Testando import do aima:")
    test_import = """
try:
    from aima.agents import Agent
    from aima.search import Problem
    print("   ✅ aima.agents e aima.search OK")
except ImportError as e:
    print(f"   ❌ Erro: {e}")
    print("\n💡 Solução:")
    print("   1. pip uninstall aima -y")
    print("   2. pip install aima==2023.2.6")
    print("   3. Ou: pip install --user aima==2023.2.6")
"""
    subprocess.run([sys.executable, "-c", test_import])
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    diagnostico()