import os
import xml.etree.ElementTree as ET

def extrair_informacoes(arquivo_xml, tags):
    tree = ET.parse(arquivo_xml)
    root = tree.getroot()

    # Define the namespace
    ns = {'ns': 'http://graphml.graphdrawing.org/xmlns'}

    data = {}

    for tag in tags:
        # Include the namespace in the tag
        elementos = root.findall('.//ns:data[@key="{}"]'.format(tag), ns)
        for elemento in elementos:
            texto = elemento.text
            if texto:
                data[tag] = texto

    return data

def create_metadata_file(data, filename):
    metadata = ET.Element('test-metadata')

    for key, value in data.items():
        ET.SubElement(metadata, key).text = value

    tree = ET.ElementTree(metadata)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def create_testcase_file(data, filename):
    testcase = ET.Element('testcase')
    testcase.set('coversError', 'true')

    for value in data.get('assumption', '').split('=='):
        ET.SubElement(testcase, 'input').text = value.strip()

    tree = ET.ElementTree(testcase)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

tags = [
    'sourcecodelang',
    'producer',
    'specification',
    'programfile',
    'programhash',
    'architecture',
    'assumption'
]

arquivo_xml = 'witness.graphml'

# Create the directory if it doesn't exist
if not os.path.exists('testsuite'):
    os.makedirs('testsuite')

data = extrair_informacoes(arquivo_xml, tags)
create_metadata_file(data, os.path.join('testsuite', 'metadata.xml'))
create_testcase_file(data, os.path.join('testsuite', 'testcase.xml'))
