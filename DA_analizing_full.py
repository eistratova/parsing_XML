from tabnanny import filename_only
import xml.etree.ElementTree as ET
import os
import stat
from os import listdir
from os.path import isfile, join
import re

# import functions    this file have next functions: 
'''
def file_len(fname):
    if os.stat(fname).st_size > 0:
        with open(fname, encoding="utf8") as f:
            for i, l in enumerate(f):
                pass
    else :
        return 0
    return i + 1
'''

dir= ('/Users/ekaterina/data4repos/')

files_folder = dir + 'xml'

res_file_path = join(files_folder, 'res.xml')

# получаем список файлов из дирректории
files = [join(files_folder, f) for f in listdir(files_folder) if isfile(join(files_folder, f))]
if res_file_path in files: files.remove(res_file_path)

print("Found following files:", files)

assert len(files)>1, "Files amount is less than 2"

def file_len(fname):
    if os.stat(fname).st_size > 0:
        with open(fname, encoding="utf8") as f:
            for i, l in enumerate(f):
                pass
    else :
        return 0
    return i + 1

functions = file_len(fname)

trees = []
total_file_lines = 0
for filename in files:
    print(f'Parsing file {filename}')
    filelen = functions.file_len(filename)
    print(f'\t {filelen} lines detected')
    total_file_lines += filelen
    xml_tree = ET.parse(filename)
    trees.append(xml_tree)
    
'''
    import pandas as pd
import xml.etree.ElementTree as ET
import io
def iter_docs(author):
    author_attr = author.attrib
    for doc in author.iter('document'):
        doc_dict = author_attr.copy()
        doc_dict.update(doc.attrib)
        doc_dict['data'] = doc.text
        yield doc_dict
xml_data = io.StringIO(u'''YOUR XML STRING HERE''')
etree = ET.parse(xml_data) #create an ElementTree object
doc_df = pd.DataFrame(list(iter_docs(etree.getroot())))
If there are multiple authors in your original document or the root of your XML is not an author, then I would add the following generator:
def iter_author(etree):
    for author in etree.iter('author'):
        for row in iter_docs(author):
            yield row
and change doc_df = pd.DataFrame(list(iter_docs(etree.getroot()))) to doc_df = pd.DataFrame(list(iter_author(etree)))
Have a look at the ElementTree tutorial provided in the xml library documentation.


Here is another way of converting a xml to pandas data frame. For example i have parsing xml from a string but this logic holds good from reading file as well.
import pandas as pd
import xml.etree.ElementTree as ET
xml_str = '<?xml version="1.0" encoding="utf-8"?>\n<response>\n <head>\n  <code>\n   200\n  </code>\n </head>\n <body>\n  <data id="0" name="All Categories" t="2018052600" tg="1" type="category"/>\n  <data id="13" name="RealEstate.com.au [H]" t="2018052600" tg="1" type="publication"/>\n </body>\n</response>'
etree = ET.fromstring(xml_str)
dfcols = ['id', 'name']
df = pd.DataFrame(columns=dfcols)
for i in etree.iter(tag='data'):
    df = df.append(
        pd.Series([i.get('id'), i.get('name')], index=dfcols),
        ignore_index=True)
df.head()



'''

