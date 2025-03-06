import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do arquivo CSV
df = pd.read_csv('results.csv')

# Filtra os dados para as linhas cujo scope_type seja "Global"
df_global = df[df['scope_type'] == 'Global']

# Calcula a média dos dados globais (ou utiliza a única linha disponível)
global_means = df_global.mean(numeric_only=True)

# Define as métricas:
left_metrics = ['UNKNOWN', 'programas>=360']
right_metrics = ['media_excl_360', 'media_incl_360']

left_values = [global_means[m] for m in left_metrics]
right_values = [global_means[m] for m in right_metrics]

left_x = [0, 1]
right_x = [2, 3]

fig, ax = plt.subplots(figsize=(8, 6))

# Plota as barras do grupo esquerdo no eixo principal
bars_left = ax.bar(left_x, left_values, color='navy')

# Cria o segundo eixo y para o grupo direito
ax2 = ax.twinx()
bars_right = ax2.bar(right_x, right_values, color='cornflowerblue')

# Configura os rótulos do eixo x
ax.set_xticks(left_x + right_x)
ax.set_xticklabels(left_metrics + right_metrics, rotation=20)

# Adiciona linha vertical separadora entre os grupos
ax.axvline(x=1.5, color='black', linestyle='--')

# Define limites dos eixos y
left_limit = 1217
right_limit = 360.000

ax.set_ylim(0, left_limit)
ax2.set_ylim(0, right_limit)

# Anota os valores sobre as barras do grupo esquerdo
for bar, metric in zip(bars_left, left_metrics):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom', fontsize=14)

# Anota os valores sobre as barras do grupo direito
for bar, metric in zip(bars_right, right_metrics):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height, f'{height:.3f}', ha='center', va='bottom', fontsize=14)

# Adiciona os contadores para os limites dos eixos
ax.text(0.02, 0.95, f'Total de programas: {left_limit:.0f}', transform=ax.transAxes, verticalalignment='top', color='red', fontsize=14)
ax2.text(0.98, 0.95, f'Tempo de exec: {right_limit:.3f}', transform=ax2.transAxes, verticalalignment='top', horizontalalignment='right', color='red', fontsize=14)

ax.set_title("Resultados Globais da Ferramenta", fontsize=16)
ax.set_ylabel("Programas executados", fontsize=16)
ax2.set_ylabel("Tempos de execução", fontsize=16)

plt.tight_layout()
plt.show()
