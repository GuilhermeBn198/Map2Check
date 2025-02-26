import matplotlib.pyplot as plt

# Dados das torres
categorias = ['FALSE', 'TRUE', 'UNKNOWN', 'COV=0.0', 'COV>0.0']
valores = [288,	 702,	661,	724,	265]

# Definir cores para as torres
cores = ['blue', 'blue', 'orange', 'grey', 'grey']

# Altura máxima do gráfico (valor de total_program_files)
altura_max = 1651

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
barras = plt.bar(categorias, valores, color=cores)

# Definir título e rótulos dos eixos com fontes ajustadas
plt.title('Programas executados', fontsize=18)
plt.xlabel('Resultados', fontsize=16)
plt.ylabel('Total de programas', fontsize=16)

# Ajustar tamanho dos rótulos do eixo x (com rotação de 10 graus) e eixo y
plt.xticks(fontsize=14, rotation=10)
plt.yticks(fontsize=14)

# Definir a altura máxima do gráfico (eixo y)
plt.ylim(0, altura_max)

# Exibir os valores acima de cada barra
for barra in barras:
    y_valor = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, y_valor + 10, 
             str(y_valor), ha='center', va='bottom', fontsize=14)

# Adicionar anotação com o valor máximo do eixo y (total_program_files)
plt.text(0.95, 0.95, f'Max: {altura_max}', transform=plt.gca().transAxes,
         ha='right', va='top', fontsize=16, fontweight='bold', color='green')

# Exibir o gráfico
plt.show()
