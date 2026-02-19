# 🏦 La Casa de Papel - O Roubo à Casa da Moeda

Um simulador interativo em Python inspirado na série *La Casa de Papel*. Neste projeto, o objetivo é guiar o "Professor" pela Casa da Moeda, capturar a joia e escapar pelo ponto de fuga sem ser pego pela polícia.

Este projeto é também uma aplicação prática de **Inteligência Artificial**, utilizando a biblioteca AIMA (*Artificial Intelligence: A Modern Approach*) para demonstrar o funcionamento de algoritmos de busca em espaços de estados dinâmicos.

## 📖 Inspiração Acadêmica: O Mundo do Wumpus (AIMA)

A arquitetura e a lógica deste projeto foram fortemente inspiradas em um dos problemas mais clássicos da Inteligência Artificial: o **Mundo do Wumpus** (*Wumpus World*), apresentado no renomado livro *Artificial Intelligence: A Modern Approach* (Stuart Russell e Peter Norvig).

* **O Ambiente:** Assim como a caverna do Wumpus é representada por um grid bidimensional isolado, nosso jogo utiliza a planta da Casa da Moeda mapeada em coordenadas `(x, y)`.
* **O Objetivo:** No problema original, o agente precisa navegar pela caverna, encontrar uma barra de ouro, usar a ação *Grab* para pegá-la e retornar são e salvo para a entrada na coordenada `[1,1]`. No nosso caso, o Professor pega a joia e deve voltar ileso para o ponto `(0,0)`.
* **Os Obstáculos e Ameaças:** Onde o livro utiliza poços mortais (abismos físicos) e o temível monstro Wumpus, nós implementamos paredes estáticas (`1`) e um Policial dinâmico (`4`) com rota de patrulha programada.
* **Espaço de Estados Dinâmico:** Uma evolução em nosso projeto é a adição da variável temporal ao espaço de estados `(x, y, tem_joia, tempo)`. Como o mundo muda a cada passo com a movimentação do policial, não basta avaliar apenas a geometria; a IA calcula rotas preventivas no tempo-espaço.

Este simulador é, na prática, uma roupagem moderna para testar a estrutura de Agentes Baseados em Conhecimento e algoritmos de busca (A*) ensinados com o Mundo do Wumpus!

---

## ✨ Funcionalidades

O jogo oferece duas formas de jogar:

* **🤖 Modo IA (Busca A* Automática):** O Professor age por conta própria. A IA calcula a rota perfeita usando o algoritmo de busca A* (A-Star), prevendo a rota de patrulha da polícia, pegando a joia e traçando o caminho mais seguro até a saída.
* **🎮 Modo Manual:** Assuma o controle! Você guia o Professor pelo mapa usando o teclado, precisando desviar da polícia em tempo real.

---

## 🛠️ Pré-requisitos

Para rodar o simulador, você precisará de:
* **Python 3.10** ou superior instalado em sua máquina.
* **AIMA3** instalado em sua máquina.
* Gerenciador de pacotes **pip** ativo.

---

## 🚀 Instalação e Execução

Siga o passo a passo abaixo para configurar e rodar o projeto perfeitamente:

**Clone o repositório**
```bash
git clone [https://github.com/evellynreis/La-Casa-de-Papel.git](https://github.com/evellynreis/La-Casa-de-Papel.git)
cd La-Casa-de-Papel