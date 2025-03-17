import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carrega os dados do CSV de sumário (ex: summary_report_with_map2check.csv)
df = pd.read_csv('results.csv', decimal=',')

# Filtra a linha Global
df_global = df[df['scope_type'] == 'Global']
if df_global.empty:
    raise ValueError("Não há linha Global no CSV.")

# Como há apenas uma linha Global, extraímos os valores:
global_row = df_global.iloc[0]

# Extraindo os valores (certifique-se de que os nomes das colunas estejam corretos)
# Assumindo que:
# - o número de tarefas com resultado FALSE está em "total_FALSE"
# - a cobertura positiva está em "total_coverage_pos"
# - os contadores de map2check e true_false para KLEE e FUZZY estão nas colunas "map2check(klee)", "map2check(fuzzy)", "true_false_klee" e "true_false_fuzzy"
false_val = global_row['FALSE']
coverage_pos = global_row['coverage_pos']
mk = global_row['map2check_klee']
tfk = global_row['true_false_klee']
mf = global_row['map2check_fuzzy']
tff = global_row['true_false_fuzzy']


# Configuração dos grupos:
# Vamos usar três grupos: 'KLEE', 'FUZZY' e 'Coverage Pos'.
group_labels = ['KLEE', 'FUZZY', 'TOTAL Coverage Pos']
x = np.arange(len(group_labels))  # Posições dos grupos

bar_width = 0.35  # Largura das barras para os grupos com duas barras

# Para o grupo "KLEE": duas barras (lado a lado)
x_klee = x[0]
bar1_klee = x_klee - bar_width/2
bar2_klee = x_klee + bar_width/2

# Para o grupo "FUZZY": duas barras (lado a lado)
x_fuzzy = x[1]
bar1_fuzzy = x_fuzzy - bar_width/2
bar2_fuzzy = x_fuzzy + bar_width/2

# Para "Coverage Pos": uma barra central
x_cov = x[2]

fig, ax = plt.subplots(figsize=(10, 6))

# Plota as barras para KLEE
bars_klee1 = ax.bar(bar1_klee, mk, width=bar_width, color='dodgerblue', label='map2check(klee)')
bars_klee2 = ax.bar(bar2_klee, tfk, width=bar_width, color='lightskyblue', label='map2check(klee)_cov>0')

# Plota as barras para FUZZY
bars_fuzzy1 = ax.bar(bar1_fuzzy, mf, width=bar_width, color='darkorange', label='map2check(fuzzy)')
bars_fuzzy2 = ax.bar(bar2_fuzzy, tff, width=bar_width, color='moccasin', label='map2check(fuzzy)_cov>0')

# Plota a barra para Coverage Pos
bar_cov = ax.bar(x_cov, coverage_pos, width=bar_width, color='seagreen', label='coverage_pos')

# Desenha uma linha pontilhada para separar os grupos (entre FUZZY e Coverage Pos)
ax.axvline(x=1.5, color='black', linestyle='--', linewidth=2)

# Define o limite do eixo y baseado em false_val
ax.set_ylim(0, false_val)

# Configura os rótulos do eixo x
ax.set_xticks(x)
ax.set_xticklabels(group_labels, fontsize=12)

# Legendas dos eixos
ax.set_ylabel("Quantidade de tarefas com resultado FALSE", fontsize=14)
ax.set_xlabel("Tarefas separadas por técnicas de teste de software", fontsize=14)
ax.set_title("Resultados Globais", fontsize=16)

# Adiciona o valor do limite (FALSE) no canto superior direito do gráfico
ax.text(0.98, 0.98, f'Resultados FALSE totais: {int(false_val)}',
        transform=ax.transAxes, horizontalalignment='right',
        verticalalignment='top', color='red', fontsize=14)

# Função para anotar as barras
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)

autolabel(bars_klee1)
autolabel(bars_klee2)
autolabel(bars_fuzzy1)
autolabel(bars_fuzzy2)
autolabel(bar_cov)

# Configura a legenda
handles = [
    bars_klee1, bars_klee2,
    bars_fuzzy1, bars_fuzzy2,
    bar_cov
]
labels = [
    'map2check(klee)', 'map2check(klee)_cov>0',
    'map2check(fuzzy)', 'map2check(fuzzy)_cov>0',
    'coverage_pos'
]
ax.legend(handles, labels, fontsize=12)

plt.tight_layout()
plt.show()
