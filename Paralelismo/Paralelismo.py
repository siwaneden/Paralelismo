from collections import deque
from concurrent.futures import ThreadPoolExecutor
import time

# =====================================
# Definição de um grafo simples inicial
# =====================================
# Esse grafo serve como referência para testar a busca em largura básica.
rede = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# ===============================================================================
# Função de busca em largura (BFS), com opção de simular carga de processamento
# ===============================================================================
# A ideia é permitir simulações mais realistas adicionando pequenos delays em cada iteração.
def percorrer_largura(mapa, origem, destino, carga_simulada=False):
    fila_exploracao = deque([[origem]])
    trilhas = []

    while fila_exploracao:
        trilha_atual = fila_exploracao.popleft()
        ultimo_no = trilha_atual[-1]

        if ultimo_no == destino:
            trilhas.append(trilha_atual)
        for adjacente in mapa.get(ultimo_no, []):
            if adjacente not in trilha_atual:
                if carga_simulada:
                    time.sleep(0.001)  
                fila_exploracao.append(trilha_atual + [adjacente])
    return trilhas

# ============================================================================
# Função para explorar subgrafos de forma paralela com ThreadPoolExecutor
# ============================================================================
# Essa função permite que múltiplos fragmentos do grafo sejam analisados em paralelo.
def explorar_com_paralelismo(lista_nos, ponto_inicial, ponto_final, grafo, carga=False):
    subconjunto = {chave: valor for chave, valor in grafo.items() if chave in lista_nos}
    return percorrer_largura(subconjunto, ponto_inicial, ponto_final, carga_simulada=carga)

# ================================================================================
# TESTE EXTRA – Geração automática de grafo grande e mais denso para simulação
# ================================================================================
# Esse grafo tem 100 nós, conectados linearmente e com conexões adicionais a cada 10 nós.

def gerar_grafo_grande(n=100):
    grafo = {}
    for i in range(n):
        grafo[str(i)] = []
        if i > 0:
            grafo[str(i)].append(str(i - 1))
        if i < n - 1:
            grafo[str(i)].append(str(i + 1))
        if i % 10 == 0 and i + 10 < n:
            grafo[str(i)].append(str(i + 10)) 
    return grafo

# Instancia o grafo grande
grafo_grande = gerar_grafo_grande(100)
origem_grande = '0'
destino_grande = '99'

# ==================================================
# Fragmentação do grafo para execução paralela
# ==================================================
# As divisões têm sobreposição para evitar perda de caminhos entre origem e destino.
fragmentos_grandes = [
    [str(i) for i in range(0, 35)],
    [str(i) for i in range(30, 70)],
    [str(i) for i in range(65, 100)],
]

# ===========================================================
# Execução sequencial da busca com carga simulada
# ===========================================================
print("\n>>> GRAFO GRANDE e MODO SEQUENCIAL <<<")
inicio_seq = time.time()
rotas_seq = percorrer_largura(grafo_grande, origem_grande, destino_grande, carga_simulada=True)
fim_seq = time.time()
print(f"Rotas encontradas: {len(rotas_seq)}")
print(f"Duracao (sequencial): {fim_seq - inicio_seq:.6f} segundos")

# ===========================================================
# Execução paralela da busca com threads e fragmentação
# ===========================================================
print("\n>>> GRAFO GRANDE e MODO PARALELO <<<")
inicio_paralelo = time.time()
respostas = []

with ThreadPoolExecutor() as executor:
    tarefas = [
        executor.submit(explorar_com_paralelismo, fragmento, origem_grande, destino_grande, grafo_grande, carga=True)
        for fragmento in fragmentos_grandes
    ]
    for tarefa in tarefas:
        respostas.extend(tarefa.result())

# ====================================================
# Filtra rotas duplicadas que podem ter vindo dos fragmentos sobrepostos
# ====================================================
rotas_unicas = []
for rota in respostas:
    if rota not in rotas_unicas:
        rotas_unicas.append(rota)

fim_paralelo = time.time()
print(f"Rotas encontradas: {len(rotas_unicas)}")
print(f"Duracao (paralelo): {fim_paralelo - inicio_paralelo:.6f} segundos")

# ====================================================
# Comparativo final de desempenho entre os dois modos
# ====================================================

print("\n=== COMPARACAO FINAL PARALELISMO ===")
print(f"Sequencial: {fim_seq - inicio_seq:.6f} segundos")
print(f"Paralelo:   {fim_paralelo - inicio_paralelo:.6f} segundos")
print(f"Diferenca em segundos:    {((fim_seq - inicio_seq) - (fim_paralelo - inicio_paralelo)):.6f} s")
print(f"Reducao:    {((fim_seq - inicio_seq) / (fim_paralelo - inicio_paralelo)):.2f} vezes menor")
