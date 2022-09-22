from email.utils import format_datetime
from itertools import count
from sys import displayhook
import xml.etree.ElementTree as ET
import pandas as pd
import glob # Библиотека для получения списка файлов
import os
import stat
from os import listdir # Библиотека для получения списка файлов
from os.path import isfile, join

# text processing libraries
import re
import string
import nltk
from nltk.corpus import stopwords
from datetime import date, datetime, time
import plotly.express as px

# Библиотеки для визуализации
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import datetime
from cloud_ml.storage.api import Storage
# To retrieve application id and secret:
# 1. Go to link: https://oauth.yandex.ru/client/new
# 2. Choose 'Web services'
# 3. Paste into 'Callback URI': https://oauth.yandex.ru/verification_code
# 4. Set up permissions on yandex disk
disk = Storage.ya_disk(application_id='222df4e7e505495192f2b25ef199b9d7', application_secret='be1807c400774a5c9a93cacb8c8771b9')
# downloading contents of the remote directory into the local one
#disk.get_dir('test-dir', 'test')

print(datetime.datetime.now())

dir_source = 'D-ML/Datasets/AiFatigueDetection/Fatigue2classes/2classesDimoza/'


dir_target = '.'
#dir_target = 'data2classes/4500-0-1.png'

# disk.get(dir_source, dir_target)


print("_"*80)
print("Стартует загрузка данных из " + dir_source + " в /" + dir_target)

disk.get_dir(dir_source,dir_target )

print("Загрузка дата-сета на локальной диск виртуальной машины завершена!")
print("="*80)
print(datetime.datetime.now())

import shutil
shutil.disk_usage("data2classes")

import os
print(os.getcwd())

# Обозначаем путь нахождения XML файлов 
# path = '/Users/ekaterina/data4repos/xml'
path = '/Users/ekaterina/github_repos/parsing_XML/xml'
'''
# Еще можно так получить список файлов, но в данном случае нельзя указать расширение файла (например xml)
list_of_files=os.listdir(path)
print('Список всех файлов: ',len(list_of_files))
'''
# Получаем список файлов
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
# Мы включим type,ccAgentID, ccDeviceID, timestamp, caller

print('+'*80)
df_1 = pd.DataFrame()
df = pd.DataFrame()
i=0
list_keywords=[]
print()

for file in list_of_files:
    # file_path=path+file  - в оригинале(у нас path прописан path = '/Users/ekaterina/github_repos/parsing_XML/xml' поэтому происходит дублирование - path+path+file - выдает ошибку. В связи с этим надо оставить file_path=file)
    print("Директория:\n", path)
    print('Файл:\n', file)
    # print('Путь к файлу:\n'+file_path)
    print('~'*40)
    tree = ET.parse(file)
    root = tree.getroot()
# Формируем колонки:
    trial = {}

    trial['type'] = root.find('channel').text
    trial['ccAgentID'] = root.find('channel').text
    trial['ccDeviceID'] = root.find('channel').text

# Переводим строковое значение времени в datestamp
    date_string = root.find('timestamp').text
    format_datetime = pd.to_datetime(date_string)
    format_date = pd.to_datetime(date_string).date()
    format_time = pd.to_datetime(date_string).time()
    #print(format_date) проверка 

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
        trial['datetime'] = format_datetime    
    else:
        trial['datetime'] = ''

    if root.find('timestamp') != None:
        trial['date'] = format_date   
    else:
        trial['date'] = ''

    if root.find('timestamp') != None:
        trial['time'] = format_time   
    else:
        trial['time'] = ''

    df = pd.DataFrame(trial,index=[i])
    i=i+1

    df_1 = pd.concat([df_1, df])
print(df_1.tail(10))
print('ИНФО',df_1.info())

print('Кол-во записей\n',len(df_1))

print('Кол-во уникальных агентов\n', len(df_1['ccAgentID'].unique()))

print('Кол-во дней записи\n', len(df_1['date'].unique()))

df_1['date'] = pd.to_datetime(df_1['date'])

print(df_1.head())

# Округляем до часов. С помощью функции df_1['hour'] = df_1['datetime'].dt.hour получаем данные в нужном формате INT

df_1['hour'] = df_1['datetime'].dt.hour
print("Округление hours function:/n", df_1['hour'])
df_1.info()

# Округляем datetime до минут - просто для тренировки
df_1['datetime'] = df_1['datetime'].dt.round('min')
print("Округление минуты:/n", df_1['datetime'])

# Для постройки графика по распределению звонков по агентам считаем кол-во агентов
count=df_1['ccAgentID'].value_counts()
print("Количество звонков по каждому агенту:/n",count)

df_1['ccAgentID'].value_counts().plot(kind='bar', label='agent count')
plt.legend()
plt.title('Распределение звонков ccAgentID')
#plt.show()
#print(df_1)

df.datetime = pd.to_numeric(df.datetime, errors='coerce').fillna(0).astype(np.int64)
df.time = pd.to_numeric(df.time, errors='coerce').fillna(0).astype(np.int64)
df_1.info()
df_1['type'].value_counts().plot(kind='bar', label='time', figsize = (15,6), title = 'Количество calls')
plt.legend()
plt.ylabel('Количество calls')
# plt.show()

#Построение графика "Распределение звонков по часам"

df_1['hour'].hist(bins=50, figsize = (15,6))
plt.title('Распределение звонков по времени(часам)')
plt.ylabel('Количество звонков')
plt.xlabel('Время звонка (час)')
#plt.show()

# Распределение звонков во времени
import plotly.express as px
df_1['hour'].plot(kind='bar', label='hour', figsize = (15,6), title = 'dispercia calls')
plt.legend()
plt.ylabel('dispercia calls in time')
#plt.show()

#games.groupby('name')['year_of_release'].sum()
Agent_hour_min = df_1.groupby('ccAgentID')['hour'].min()
Agent_hour_max = df_1.groupby('ccAgentID')['hour'].max()
print("Час начала рабочего дня/n:",Agent_hour_min)
print("Час начала рабочего дня/n:", Agent_hour_max)

duration = Agent_hour_max-Agent_hour_min
print("Продолжительность рабочего дня агентов:",duration)
