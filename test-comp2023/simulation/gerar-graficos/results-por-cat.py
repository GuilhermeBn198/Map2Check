import matplotlib.pyplot as plt

# Dados para cada subcategoria
dados = [
    {
        "scope_name": "ReachSafety-Arrays",
        "total_program_files": 100,
        "FALSE": 81,
        "TRUE": 2,
        "UNKNOWN": 16,
        "COV=0.0": 70,
        "COV>0.0": 14
    },
    {
        "scope_name": "ReachSafety-BitVectors",
        "total_program_files": 9,
        "FALSE": 5,
        "TRUE": 0,
        "UNKNOWN": 4,
        "COV=0.0": 3,
        "COV>0.0": 2
    },
    {
        "scope_name": "ReachSafety-Loops",
        "total_program_files": 125,
        "FALSE": 61,
        "TRUE": 10,
        "UNKNOWN": 53,
        "COV=0.0": 37,
        "COV>0.0": 35
    },
    {
        "scope_name": "ReachSafety-Heap",
        "total_program_files": 53,
        "FALSE": 12,
        "TRUE": 0,
        "UNKNOWN": 41,
        "COV=0.0": 3,
        "COV>0.0": 9
    },
]

# Torres e definição de cores
torres = ['FALSE', 'TRUE', 'UNKNOWN', 'COV=0.0', 'COV>0.0']
cores = ['blue', 'blue', 'orange', 'grey', 'grey']

# Cria um grid 2x2 para os subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for ax, grupo in zip(axes, dados):
    # Obtém os valores para cada torre e o total_program_files
    valores = [grupo[t] for t in torres]
    total_pf = grupo["total_program_files"]

    # Plota as barras com as cores definidas
    barras = ax.bar(torres, valores, color=cores)
    
    # Configura título e rótulos dos eixos com os tamanhos de fonte especificados
    ax.set_title(grupo["scope_name"], fontsize=18)
    # ax.set_xlabel("Subcategorias", fontsize=16)
    ax.set_ylabel("Total de programas", fontsize=16)
    
    # Rotaciona os rótulos do eixo x em 10 graus e ajusta a fonte
    plt.setp(ax.get_xticklabels(), rotation=15, fontsize=16)
    plt.setp(ax.get_yticklabels(), fontsize=16)
    
    # Define o limite do eixo y igual a total_program_files
    ax.set_ylim(0, total_pf)
    
    # Exibe o valor máximo (total_program_files) no canto superior direito do subplot
    ax.text(0.95, 0.95, f'Max: {total_pf}', transform=ax.transAxes,
            ha='right', va='top', fontsize=16, color='green')
    
    # Exibe os números acima de cada barra com fonte 16
    for barra in barras:
        y_valor = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, y_valor + total_pf*0.02,
                str(y_valor), ha='center', va='bottom', fontsize=16)

plt.tight_layout()
plt.show()
