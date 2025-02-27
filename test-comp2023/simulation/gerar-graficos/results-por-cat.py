import matplotlib.pyplot as plt

# Dados para cada subcategoria
dados = [
    {
        "scope_name": "ReachSafety-Arrays",
        "total_program_files": 531,
        "FALSE": 95,
        "TRUE": 232,
        "UNKNOWN": 204,
        "COV=0.0": 241,
        "COV>0.0": 86
    },
    {
        "scope_name": "ReachSafety-BitVectors",
        "total_program_files": 83,
        "FALSE": 16,
        "TRUE": 20,
        "UNKNOWN": 47,
        "COV=0.0": 23,
        "COV>0.0": 13
    },
    {
        "scope_name": "ReachSafety-ControlFlow",
        "total_program_files": 156,
        "FALSE": 28,
        "TRUE": 29,
        "UNKNOWN": 99,
        "COV=0.0": 21,
        "COV>0.0": 36
    },
    {
        "scope_name": "ReachSafety-Loops",
        "total_program_files": 881,
        "FALSE": 149,
        "TRUE": 421,
        "UNKNOWN": 311,
        "COV=0.0": 439,
        "COV>0.0": 130
    }
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
