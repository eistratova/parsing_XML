import xml.etree.ElementTree as ET 
import pandas as pd 
 
dir= ('/Users/ekaterina/data4repos/AIFD')
xml_file = '/node_7_domain_0_nauss_7_1645875244_3355116.xml'

xml_file_1 = dir+xml_file

xml_data = open(xml_file_1, 'r').read() # Read file 
root = ET.XML(xml_data) # Parse XML 
 
data = [] 
cols = [] 
for i, child in enumerate(root): 
    data.append([subchild.text for subchild in child])
    
    cols.append(child.tag) 
 
df = pd.DataFrame(data).T # Write in DF and transpose it 
df.columns = cols # Update column names 
print(df) 

memoryElem = root.find('channel')
#print(memoryElem.text)        # element text


print("Агент ID:", memoryElem.get('ccAgentID')) # attribute





''''
# Here is another way of converting a xml to pandas data frame. For example i have parsing xml from a string but this logic holds good from reading file as well.
import pandas as pd
import xml.etree.ElementTree as ET
dir= ('/Users/ekaterina/data4repos/AIFD')
xml_file = '/node_7_domain_0_nauss_7_1645875244_3355116.xml'
xml_str = '<?xml version="1.0" encoding="utf-8"?>\n<analysisTask cc-task="7_0_7_1645875244_3355116"><timestamp>2022-04-27 06:57:50.000 MSK</timestamp><filename>node_7_domain_0_nauss_7_1645875244_3355116.wav</filename><channel type="a" ccAgentID="abzalov" ccDeviceID="abzalov" disconnect="true"/><channel type="c" value="79223590903" caller="true"/></analysisTask>  
### <data id="0" name="All Categories" t="2018052600" tg="1" type="category"/>\n  <data id="13" name="RealEstate.com.au [H]" t="2018052600" tg="1" type="publication"/>\n </body>\n</response>'
etree = ET.fromstring(xml_str)                                           
dfcols = ['timestamp', 'ccAgentID']
df = pd.DataFrame(columns=dfcols)
for i in etree.iter(tag='analysisTask'):
    df = df.append(
        pd.Series([i.get('timestamp'), i.get('ccAgentID')], index=dfcols),
        ignore_index=True)
df.head()
'''