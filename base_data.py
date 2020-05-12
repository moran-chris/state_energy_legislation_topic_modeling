import numpy as np 
import pandas as pd
from bs4 import BeautifulSoup
import codecs 
import requests 


#doc = np.genfromtxt('Prescription Drug Bills - Sheet1.csv',dtype = str,delimiter = '\t')
doc = np.genfromtxt('Prescription Drug Bills - 2020.csv',dtype = str,delimiter = '\t')


rows = []
row = []
for element in doc:
    if element[:8] == "History:":
        rows.append(row)
        row = []
    else:
        row.append(element)


df = pd.DataFrame(columns = ['bill_id','title','year','status','Author','topics','summary','associated_bills','date_of_last_action'])


df_row = {}
for item in rows:
    df_row = {'bill_id':item.pop(0), 'year' : item.pop(0), 'title':item.pop(0)}
    for element in item:
        idx = element.find(':')
        if idx != -1:
            df_row[element[:idx]] = element[idx + 2:]
    df = df.append(df_row, ignore_index = True)
    df_row = {}


data = codecs.open("view-source_https___www.ncsl.org_research_health_prescription-drug-statenet-database_no_DC.aspx.html", "r", "utf-8")
soup = BeautifulSoup(data.read(),'html.parser')
links = [list(link.children)[0] for link in soup.find_all('a', href=True)]

bill_links = []
for link in links:
    if 'custom.statenet.com' in link:
        bill_links.append(link)

page = requests.get(bill_links[0])
soup = BeautifulSoup(page.content,'html.parser')