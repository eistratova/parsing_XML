# Парсинг XML и Получение атрибута из него
import xml.etree.ElementTree as ET

dir= ('/Users/ekaterina/data4repos/AIFD')
xml_file = '/node_7_domain_0_nauss_7_1645875244_3355116.xml'

tree = ET.parse(dir+xml_file)
root = tree.getroot()

print()
print('_'*80)
print("Корневой элемент XML-файла: ",root)
print('~ '*40)
print("Тэг корневого элемент XML-файла: ",root.tag)
print('_'*80)

print()
print('ДОЧЕРНИЕ УЗЛЫ')
for child in root:
    print(child.tag, child.attrib)

print('Root[2] : ',root[2].text)
print('Root tag: ', root.tag)
print('Root [1] attribut:', root[1].attrib)

print('_'*80)

for channel in root.iter('channel'):
     print(channel.attrib)

print('*'*80)
print('Получение атрибута элемента "ccAgentID"')

memoryElem = tree.find('channel')
#print(memoryElem.text)        # element text
print("Агент ID:", memoryElem.get('ccAgentID')) # attribute


'''
Вариант с минидомом

import xml.dom.minidom as minidom
doc = minidom.parse(filename)

memoryElem = doc.getElementsByTagName('memory')[0]
print ''.join( [node.data for node in memoryElem.childNodes] )
print memoryElem.getAttribute('unit')
'''

