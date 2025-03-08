import matplotlib.pyplot as plt

# Dados das torres
categorias = ['Map2Check FALSE', 'ESBMC FALSE', 'KLEE FALSE', 'FuseBMC FALSE']
valores = [ 210, 195, 713, 926]

# Definir cores para as torres (apenas 4 cores, pois são 4 categorias)
cores = ['blue', 'green', 'yellow', 'orange']

# Altura máxima do gráfico (valor de total_program_files)
altura_max = 1216

# Criar o gráfico de barras para as torres principais
plt.figure(figsize=(10, 6))
barras = plt.bar(categorias, valores, color=cores)

# Adicionar uma segunda torre (barra interna) somente na primeira torre ("Map2Check FALSE")
# Pega a primeira barra (índice 0)
primeira_barra = barras[0]
x = primeira_barra.get_x()
largura = primeira_barra.get_width()

# Configurar posição e largura para que a segunda torre fique "dentro" da primeira
margem = 0.2 * largura           # margem para centralizar a barra interna
largura_interna = 0.6 * largura    # largura menor para evidenciar que é interna

# Desenhar a segunda torre com valor 65
plt.bar(x + margem, 65, width=largura_interna, color='red')

# Exibir os valores acima de cada torre externa
for barra in barras:
    y_valor = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, y_valor + 10, 
             str(y_valor), ha='center', va='bottom', fontsize=14)

# Exibir o valor da segunda torre centralizado na sua barra interna
plt.text(x + margem + largura_interna/2, 65/2, '65', ha='center', va='center', 
         color='white', fontsize=16, fontweight='bold')

# Configura título e rótulos dos eixos com fontes ajustadas
plt.title('Programas executados', fontsize=18)
plt.ylabel('Total de programas', fontsize=16)

# Ajustar os rótulos dos eixos x e y
plt.xticks(fontsize=14, rotation=10)
plt.yticks(fontsize=14)

# Definir a altura máxima do gráfico (eixo y)
plt.ylim(0, altura_max)

# Adicionar anotação com o valor máximo do eixo y (total_program_files)
plt.text(0.95, 0.95, f'Max: {altura_max}', transform=plt.gca().transAxes,
         ha='right', va='top', fontsize=16, fontweight='bold', color='green')

# Exibir o gráfico
plt.show()
