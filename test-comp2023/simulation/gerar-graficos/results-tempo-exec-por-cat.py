import pandas as pd
import matplotlib.pyplot as plt
import math

# Carrega os dados do arquivo CSV
df = pd.read_csv('results.csv')

# Lista com os scope_name desejados
selected_categories = ["ReachSafety-Arrays", "ReachSafety-BitVectors", "ReachSafety-Loops", "ReachSafety-XCSP"]

# Filtra os dados para as linhas cujo scope_type seja "Category" e scope_name seja um dos desejados
df_category = df[(df['scope_type'] == 'Category') & (df['scope_name'].isin(selected_categories))]

# Obtém as categorias únicas a partir da coluna 'scope_name'
categories = df_category['scope_name'].unique()
num_categories = len(categories)

# Define as métricas:
# Grupo esquerdo (eixo y esquerdo): contagens (UNKNOWN, programas>=360)
# Grupo direito (eixo y direito): tempos (media_excl_360, media_incl_360)
left_metrics = ['UNKNOWN', 'programas>=360']
right_metrics = ['media_excl_360', 'media_incl_360']

# Define grid 2x2: 2 colunas e número de linhas necessário
n_cols = 2
n_rows = math.ceil(num_categories / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6 * n_rows))
axes = axes.flatten()  # Facilita a iteração

for i, cat in enumerate(categories):
    ax = axes[i]
    # Seleciona os dados da categoria e calcula a média (caso haja mais de uma linha)
    data = df_category[df_category['scope_name'] == cat]
    means = data.mean(numeric_only=True)
    
    # Valores para os dois grupos
    left_values = [means[m] for m in left_metrics]
    right_values = [means[m] for m in right_metrics]
    
    # Define posições para as barras: 0 e 1 para o grupo esquerdo; 2 e 3 para o grupo direito
    left_x = [0, 1]
    right_x = [2, 3]
    
    # Plota as barras do grupo esquerdo no eixo principal (ax)
    bars_left = ax.bar(left_x, left_values, color='navy')
    
    # Cria o segundo eixo y para o grupo direito (tempos)
    ax2 = ax.twinx()
    bars_right = ax2.bar(right_x, right_values, color='cornflowerblue')
    
    # Configura os rótulos do eixo x (compartilhado)
    ax.set_xticks(left_x + right_x)
    ax.set_xticklabels(left_metrics + right_metrics, rotation=15)
    
    # Adiciona linha vertical separadora entre os grupos
    ax.axvline(x=1.5, color='black', linestyle='--')
    
    # Define limites dos eixos y
    left_limit = sum(left_values)  # soma entre UNKNOWN e programas>=360
    right_limit = 360
    
    ax.set_ylim(0, left_limit)
    ax2.set_ylim(0, right_limit)
    
    # Anota os valores sobre as barras (eixo esquerdo: contagens)
    for bar, metric in zip(bars_left, left_metrics):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')
    
    # Anota os valores sobre as barras (eixo direito: tempos, com três casas decimais)
    for bar, metric in zip(bars_right, right_metrics):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height, f'{height:.3f}', ha='center', va='bottom')
    
    # Adiciona "contadores" para os limites dos eixos
    ax.text(0.02, 0.95, f'Total de programas: {left_limit:.0f}', transform=ax.transAxes, verticalalignment='top', color='red')
    ax2.text(0.98, 0.95, f'Tempo de exec: {right_limit:.3f}', transform=ax2.transAxes, verticalalignment='top', horizontalalignment='right', color='red')
    
    ax.set_title(f"{cat}")
    ax.set_ylabel("Programas executados")
    ax2.set_ylabel("Tempos de execução")

# Remove subplots vazios, se houver
for j in range(i+1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
