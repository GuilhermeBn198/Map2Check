import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Carrega os dados do CSV, considerando que os números usam vírgula como separador decimal
df = pd.read_csv('results.csv', decimal=',')
df.columns = df.columns.str.strip()

# Subcategorias específicas desejadas
selected_subcats = ["ReachSafety-Arrays", "ReachSafety-BitVectors", "ReachSafety-Loops", "ReachSafety-Heap"]

# Filtra as linhas que não são Global e cujo scope_name está na lista de subcategorias selecionadas.
df_sub = df[(df['scope_type'].str.lower() != 'global') & (df['scope_name'].isin(selected_subcats))]

# Se houver mais de uma linha por subcategoria, vamos usar a média
n_sub = len(selected_subcats)
n_cols = 2
n_rows = math.ceil(n_sub / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6 * n_rows))
axes = axes.flatten()

# Rótulos para cada barra
bar_labels = ['map2check(klee)', 'map2check(klee)_cov>0', 'map2check(fuzzy)', 'map2check(fuzzy)_cov>0', 'TOTAL Coverage Pos']

for i, subcat in enumerate(selected_subcats):
    ax = axes[i]
    # Seleciona a linha do dataframe correspondente à subcategoria
    data = df_sub[df_sub['scope_name'] == subcat]
    if data.empty:
        print(f"Subcategoria {subcat} não encontrada no CSV.")
        continue
    # Se houver múltiplas linhas, utiliza a média
    row = data.mean(numeric_only=True)
    
    # Extrai os valores numéricos
    false_val = float(row['FALSE'])
    mk = float(row['map2check_klee'])
    tfk = float(row['true_false_klee'])
    mf = float(row['map2check_fuzzy'])
    tff = float(row['true_false_fuzzy'])
    coverage_val = float(row['coverage_pos'])
    
    # Valores em ordem dos rótulos
    values = [mk, tfk, mf, tff, coverage_val]
    
    # Posições para as 5 barras
    x = np.arange(len(bar_labels))
    bar_width = 0.8
    
    # Plota as barras
    bars = ax.bar(x, values, width=bar_width, color=['dodgerblue', 'lightskyblue', 'darkorange', 'moccasin', 'seagreen'])
    
    # Desenha uma linha pontilhada para separar a coluna coverage_pos das demais
    # A linha será desenhada entre as barras de índice 3 e 4 (x = 3.5)
    ax.axvline(x=3.5, color='black', linestyle='--', linewidth=2)
    
    # Configura os rótulos do eixo x com rotação de 15°
    ax.set_xticks(x)
    ax.set_xticklabels(bar_labels, rotation=20, fontsize=11)
    
    # Define o limite do eixo y igual ao valor de FALSE (limite superior)
    ax.set_ylim(0, false_val)
    
    # Adiciona anotações sobre cada barra
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)
    
    # Exibe o valor de FALSE (limite) no canto superior direito
    ax.text(0.98, 0.98, f'Resultados FALSE totais: {int(false_val)}', transform=ax.transAxes,
            horizontalalignment='right', verticalalignment='top', color='red', fontsize=16)
    
    # Configura título e rótulo do eixo y
    ax.set_title(f"Subcategoria: {subcat}", fontsize=14, fontweight='bold')
    ax.set_ylabel("Tarefas com resultado FALSE", fontsize=12)

# Remove subplots vazios, se houver
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
