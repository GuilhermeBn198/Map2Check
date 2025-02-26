import matplotlib.pyplot as plt

# Dados das torres
categorias = ['total_FALSE', 'total_TRUE', 'total_coverage_pos','total_coverage_0.0', 'total_UNKNOWN']
valores = [288, 702, 265, 724, 661]

# Definir cores para as torres
cores = ['blue', 'blue', 'green', 'red', 'grey']

# Altura máxima do gráfico (valor de total_program_files)
altura_max = 1651

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
barras = plt.bar(categorias, valores, color=cores)

# Definir título e rótulos dos eixos
plt.title('Programas executados',fontsize=18)
plt.xlabel('Resultados',fontsize=16)
plt.ylabel('Total de programas',fontsize=16)

# Ajustar tamanho dos rótulos do eixo x e girá-los para melhor visualização
plt.xticks(fontsize=14, rotation=10)
plt.yticks(fontsize=14)

# Definir a altura máxima do gráfico
plt.ylim(0, altura_max)

# Exibir os valores acima de cada barra
for barra in barras:
    y_valor = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, y_valor + 10, str(y_valor), ha='center', va='bottom', fontsize=14)

# Exibir o gráfico
plt.show()
