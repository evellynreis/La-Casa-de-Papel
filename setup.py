# setup.py (corrigido)
import subprocess
import sys
import os

def setup_project():
    """Configura o ambiente do projeto automaticamente"""
    
    print("🔧 Configurando o Projeto La Casa de Papel...")
    print("=" * 50)
    
    # Verifica versão do Python
    print(f"\n📌 Python: {sys.version}")
    
    # Atualiza o pip primeiro
    print("\n📌 Atualizando pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Instala dependências
    print("\n📦 Instalando dependências...")
    
    # Primeiro tenta sem --user
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except:
        # Se falhar, tenta com --user
        print("   ⚠ Tentando com --user...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"])
    
    # Verifica instalação
    print("\n🔍 Verificando instalação...")
    try:
        # Testa import do aima
        test_code = """
try:
    from aima.agents import Agent, Environment
    from aima.search import Problem, astar_search
    print("✅ aima encontrado!")
    print(f"   - agents: OK")
    print(f"   - search: OK")
except ImportError as e:
    print(f"❌ Erro: {e}")
    exit(1)
"""
        result = subprocess.run(
            [sys.executable, "-c", test_code],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            raise Exception("Falha na verificação")
            
    except Exception as e:
        print(f"\n❌ Erro na verificação: {e}")
        print("\n💡 Soluções possíveis:")
        print("   1. Execute manualmente: pip install aima==2023.2.6")
        print("   2. Ou: pip install --user aima==2023.2.6")
        print("   3. Verifique se os arquivos __init__.py existem")
        return
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("\n📋 Para executar o projeto:")
    print("    python main.py")
    print("\n📋 Para executar os testes:")
    print("    pytest tests/ -v")

if __name__ == "__main__":
    setup_project()