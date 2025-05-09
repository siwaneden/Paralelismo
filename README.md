# 🔄 Busca em Largura com Execução Paralela em Grafos

Este projeto implementa uma comparação prática entre a **execução sequencial** e a **execução paralela** de um algoritmo de busca em largura (BFS) em grafos, com foco em cenários onde o paralelismo realmente oferece ganhos de desempenho.

## 🧠 Motivação

Apesar de o paralelismo prometer maior velocidade de execução, ele nem sempre é eficaz em tarefas pequenas ou rápidas. Aqui, mostro **quando e por que o paralelismo compensa**, utilizando simulações com grafos grandes e carga artificial para ilustrar os efeitos reais do uso de threads.

---

## 🚀 O que o projeto faz

- Executa busca em largura (BFS) para encontrar **todos os caminhos possíveis** entre dois nós em um grafo.
- Compara o tempo de execução da busca:
  - ✅ Em modo **sequencial**.
  - ✅ Em modo **paralelo**, utilizando `ThreadPoolExecutor`.
- Simula carga computacional em cada iteração com `time.sleep` para representar tarefas reais (como I/O, cálculos, etc).
- Usa **grafos artificiais grandes** para tornar o benchmark significativo.

---

### Pré-requisitos
- Python 3.7+



