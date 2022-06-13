import pandas as pd
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import sqlite3
import networkx as nx
import matplotlib as plt



# использовую недокументированного API, пришлось долго рыться в коде странице, чтобы найти нужное
ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

url = 'https://www.chitai-gorod.ru/shops/'
params = {'format': 'json'}
r = requests.get(url, params, headers=header)
s = r.text
# Ниже использую регулярные выражения, так как без их использования выходит сложное решение
ps = re.findall(r'data-lat=(.*?)\n', s)
ps1 = re.findall(r'data-lng=(.*?)\n', s)
lat = []
lon = []
# работаю с продвинутым pandas
for i in range(1,len(ps)):
    lat.append(ps[i])
    lon.append(ps1[i])
l = pd.DataFrame({'lat':lat,'lon':lon})
l['lat'] = l['lat'].str.replace('"', '')
l['lon'] = l['lon'].str.replace('"', '')
l.to_csv('/Users/vanys/PycharmProjects/project/data.csv')

# Использую SQL  и строю граф, но в стримлит базу данных сложно подключать, поэтому там я делаю по-другому, чтобы виден был результат, но этот код работает точно также и удобнее
df=pd.read_csv('harry.csv')
conn = sqlite3.connect('harry.sqlite')
c = conn.cursor()
har = c.execute(
    """
    SELECT name, house FROM harry
    WHERE house IS NOT NULL
    """).fetchall()
ww = nx.Graph(har)
nx.draw(ww.subgraph(['Gryffindor'] + list(ww.neighbors('Gryffindor'))), with_labels=True)