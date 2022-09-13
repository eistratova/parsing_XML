import xml.etree.ElementTree as ET
import pandas as pd
import glob
import os
import stat
from os import listdir
from os.path import isfile, join

# text processing libraries
import re
import string
import nltk
from nltk.corpus import stopwords
from datetime import datetime

# path = '/Users/ekaterina/data4repos/xml'
path = '/Users/ekaterina/github_repos/parsing_XML/xml'
'''
# Еще можно так получить список файлов, но в данном случае нельзя указать расширение файла (например xml)
list_of_files=os.listdir(path)
print('Список всех файлов: ',len(list_of_files))
'''
import glob

list_of_files = glob.glob(path + '/*.xml')
print('_'*80)
print('\nСписок всех файлов:\n',list_of_files)

df = pd.DataFrame(list_of_files)
print("Дата фрейм:")
print(df)
print('_'*80)

# Чтение первого файла

file_path_file1 = os.path.join(path, list_of_files[0])
tree = ET.parse(file_path_file1)
root = tree.getroot()

print('Чтение первого файла:')
print(root.tag, root.attrib)

print('\nПуть к 1-му файлу:')
print(file_path_file1)
print()

# просмотр дочерних элементов и атрибутов
for child in root:     
    print('Дочерние элементы и атрибуты:', child.tag, child.attrib)

# просмотр всех атрибутов и элементов документа
print('\nПросмотр всех атрибутов и элементов документа:\n', ET.tostring(root, encoding='utf8').decode('utf8'))

# Теперь мы инициализируем два пустых фрейма данных, которые будут заполнены указанными выше элементами. 
# Мы включим type,ccAgentID, ccDeviceID, disconnect, value, caller

print('+'*80)
df_1 = pd.DataFrame()
df = pd.DataFrame()
i=0
list_keywords=[]
print()

for file in list_of_files:
    # file_path=path+file
    print("Директория:\n", path)
    print('Файл:\n', file)
    # print('Путь к файлу:\n'+file_path)
    print('~'*40)
    tree = ET.parse(file)
    root = tree.getroot()

    trial = {}

    trial['type'] = root.find('channel').text
    trial['ccAgentID'] = root.find('channel').text
    trial['ccDeviceID'] = root.find('channel').text

# Переводим строковое значение времени в datestamp
    date_string = root.find('timestamp').text
    format_date = pd.to_datetime(date_string)
    # print(format_date)

    if root.find('channel') != None:
        trial['type'] = tree.find('channel').get('type')
    else:
        trial['type'] = ''

    if root.find('channel') != None:
        trial['ccAgentID'] = tree.find('channel').get('ccAgentID')
    else:
        trial['ccAgentID'] = ''

    if root.find('channel') != None:
        trial['ccDeviceID'] = tree.find('channel').get('ccDeviceID')
    else:
        trial['ccDeviceID'] = ''

    if root.find('timestamp') != None:
        trial['date'] = format_date    
    else:
        trial['date'] = ''

    df = pd.DataFrame(trial,index=[i])
    i=i+1

    df_1 = pd.concat([df_1, df])
print(df_1.head())




    