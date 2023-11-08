import xml.etree.ElementTree as ET

# Função para extrair informações das tags especificadas do XML
def extrair_informacoes(arquivo_xml, tags, arquivo_saida):
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()

    with open(arquivo_saida, 'w') as saida:
        for tag in tags:
            elementos = root.findall('.//{}'.format(tag))
            for elemento in elementos:
                texto = elemento.text
                if texto:
                    saida.write('{}: {}\n'.format(tag, texto))

# Lista de tags que você deseja extrair informações
tags = [
    'sourcecodelang',
    'producer',
    'specification',
    'programfile',
    'programhash',
    'entryfunction',
    'architecture',
    'creationtime'
]

# Arquivo XML de entrada
arquivo_xml = 'seuarquivo.xml'

# Arquivo de saída
arquivo_saida = 'informacoes_extraidas.txt'

# Chame a função para extrair as informações das tags especificadas
extrair_informacoes(arquivo_xml, tags, arquivo_saida)
