from collections import deque
from concurrent.futures import ThreadPoolExecutor
import time

# =========================================
# Etapa 1 – Definição da Estrutura do Grafo
# =========================================
rede = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# ===================================================
# Etapa 2 – Caminhamento em Largura: Todos os Percursos
# ===================================================

def percorrer_largura(mapa, origem, destino):
    fila_exploracao = deque([[origem]])
    trilhas = []

    while fila_exploracao:
        trilha_atual = fila_exploracao.popleft()
        ultimo_no = trilha_atual[-1]

        if ultimo_no == destino:
            trilhas.append(trilha_atual)
        for adjacente in mapa.get(ultimo_no, []):
            if adjacente not in trilha_atual:
                proximo_trajeto = trilha_atual + [adjacente]
                fila_exploracao.append(proximo_trajeto)
    return trilhas

# ================================================
# Etapa 3 – Ação Paralela para Subgrafos Parciais
# ================================================

def explorar_com_paralelismo(lista_nos, ponto_inicial, ponto_final):
    subconjunto = {chave: valor for chave, valor in rede.items() if chave in lista_nos}
    return percorrer_largura(subconjunto, ponto_inicial, ponto_final)

# ========================================
# Etapa 4 – Execução Tradicional (Linear)
# ========================================

print("\n>>> PROCESSAMENTO SEQUENCIAL <<<")
inicio_seq = time.time()
rotas_sequenciais = percorrer_largura(rede, 'A', 'F')
fim_seq = time.time()

for rota in rotas_sequenciais:
    print("Trajeto encontrado:", rota)
print(f"Duração (modo direto): {fim_seq - inicio_seq:.20f} segundos")

# ======================================
# Etapa 5 – Execução Simultânea (Threads)
# ======================================

print("\n>>> PROCESSAMENTO CONCORRENTE <<<")

fragmentos = [
    ['A', 'B'],
    ['C', 'F'],
    ['D', 'E']
]

inicio_paralelo = time.time()
respostas = []

with ThreadPoolExecutor() as gestor:
    tarefas = [gestor.submit(explorar_com_paralelismo, fragmento, 'A', 'F') for fragmento in fragmentos]
    for tarefa in tarefas:
        saida = tarefa.result()
        respostas.extend(saida)

fim_paralelo = time.time()


rotas_distintas = []
for trajeto in respostas:
    if trajeto not in rotas_distintas:
        rotas_distintas.append(trajeto)

for caminho in rotas_distintas:
    print("Caminho detectado:", caminho)
print(f"Duração (modo concorrente): {fim_paralelo - inicio_paralelo:.20f} segundos")

# ===============================
# Etapa 6 – Comparativo Final
# ===============================

print("\n=== DESEMPENHO COMPARADO ===")
print(f"Modo direto:     {fim_seq - inicio_seq:.20f} s")
print(f"Modo paralelo:   {fim_paralelo - inicio_paralelo:.20f} s")

