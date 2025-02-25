import matplotlib.pyplot as plt

# Dados das torres
categorias = ['total_FALSE', 'total_TRUE', 'total_UNKNOWN', 'total_coverage_0.0', 'total_coverage_pos']
valores = [288, 702, 661, 724, 265]

# Definir cores para as torres
cores = ['blue', 'blue', 'blue', 'red', 'red']

# Altura máxima do gráfico (valor de total_program_files)
altura_max = 1651

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
barras = plt.bar(categorias, valores, color=cores)

# Definir título e rótulos dos eixos
plt.title('Programas executados')
plt.xlabel('Resultados')
plt.ylabel('Total de programas')

# Definir a altura máxima do gráfico
plt.ylim(0, altura_max)

# Exibir os valores acima de cada barra
for barra in barras:
    y_valor = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, y_valor + 10, str(y_valor), ha='center', va='bottom')

# Exibir o gráfico
plt.show()
