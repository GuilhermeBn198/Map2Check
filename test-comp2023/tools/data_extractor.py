import os
import xml.etree.ElementTree as ET
from datetime import datetime
import zipfile

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
        if key != 'assumption':
            ET.SubElement(metadata, key).text = value

    # Add creationtime tag
    creationtime = datetime.now().isoformat()
    ET.SubElement(metadata, 'creationtime').text = creationtime

    tree = ET.ElementTree(metadata)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

import re

def create_testcase_file(data, filename):
    testcase = ET.Element('testcase')
    testcase.set('coversError', 'true')

    for value in data:
        value = value.strip()
        number = re.findall(r'== (\d+)', value)[0]
        ET.SubElement(testcase, 'input').text = number

    tree = ET.ElementTree(testcase)
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def create_zip_file(metadata_filename, testcase_filename):
    with zipfile.ZipFile('test-suite.zip', 'w') as zipf:
        zipf.write(metadata_filename, arcname='metadata.xml')
        zipf.write(testcase_filename, arcname='testcase.xml')

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

assumptions = []
for edge in ET.parse(arquivo_xml).getroot().iter('{http://graphml.graphdrawing.org/xmlns}edge'):
    assumption_data = edge.find('{http://graphml.graphdrawing.org/xmlns}data[@key="assumption"]').text
    assumptions.append(assumption_data)

create_metadata_file(data, os.path.join('testsuite', 'metadata.xml'))
create_testcase_file(assumptions, os.path.join('testsuite', 'testcase.xml'))
create_zip_file(os.path.join('testsuite', 'metadata.xml'), os.path.join('testsuite', 'testcase.xml'))