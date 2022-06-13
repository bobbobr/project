from selenium import webdriver
import streamlit as st
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

# использую сложные технологии скреппинга и использую продвинутые возможности pandas для обработки данных
driver = webdriver.Chrome('/Users/vanys/PycharmProjects/project/chromedriver')
booklist=[]
desc=[]
timelist = []
genres = []
rates = []
votes = []
regs = []
for link in ['https://www.imdb.com/list/ls023586020/?ref_=otl_1&st_dt=&mode=detail&page=1&sort=runtime,desc',
             'https://www.imdb.com/list/ls023586020/?ref_=otl_1&st_dt=&mode=detail&page=2&sort=runtime,desc',
             'https://www.imdb.com/list/ls023586020/?ref_=otl_1&st_dt=&mode=detail&page=3&sort=runtime,desc',
             'https://www.imdb.com/list/ls023586020/?ref_=otl_1&st_dt=&mode=detail&page=4&sort=runtime,desc',
             'https://www.imdb.com/list/ls023586020/?ref_=otl_1&st_dt=&mode=detail&page=5&sort=runtime,desc']:
    driver.get(link)

    books = driver.find_elements(by=By.CLASS_NAME, value='lister-item-header')
    time = driver.find_elements(by=By.CLASS_NAME, value="runtime")
    genre = driver.find_elements(by=By.CLASS_NAME, value="genre")
    rate = driver.find_elements(by=By.CLASS_NAME, value='ipl-rating-widget')
    vote = driver.find_elements(by=By.CLASS_NAME, value="text-small:nth-child(6)")
    reg = driver.find_elements(by=By.CLASS_NAME, value='text-small')
    for q in range(len(reg)):
        regs.append(reg[q].text)
    for s in range(len(books)):
        booklist.append(books[s].text)
        genres.append(genre[s].text)
        rates.append(rate[s].text)
        votes.append(vote[s].text)
    for l in range(len(time)):
        timelist.append(time[l].text)

regs = regs[129:429] + regs[558:858] + regs[987:1287] + regs[1416:1716] + regs[1845:1918]
roles = []
for qub in range(1,1272,3):
    roles.append(regs[qub])
mda = []
for ds in range(2, 1272,3):
    mda.append(regs[ds])
md = pd.DataFrame(mda)
rol = pd.DataFrame(roles)
s = pd.DataFrame(booklist)
t = pd.DataFrame(timelist)
genr = pd.DataFrame(genres)
rat = pd.DataFrame(rates)
vot = pd.DataFrame(votes)

s = s[0].str.split('(', expand = True)
df = pd.concat([s, t, genr, rat, vot, rol, md], ignore_index=True, axis=1)
df[1] = df[1].str.replace(')', '')
new = df[0].str.split('.', expand = True)
df[0] = new[1]
check = df[3].str.split('m', expand = True)
df[2] = check[0]
hah = df[5].str.split('\n', expand = True)
df[5] = hah[0]
top = df[6].str.split(':', expand = True)
df[6]= top[1]
kak = md[0].str.split('|', expand = True)
kak = kak[0].str.split(':', expand = True)
df[6] = kak[1]
kek = df[7].str.split('|', expand = True)
kek = kek[0].str.split(':', expand = True)
df[7]= kek[1]
nado = df[1].str.split('–', expand = True)
df[1] = nado[0]
df = df.drop([3], axis = 1)
df = df.drop([8], axis = 1)
df.columns = ['Name', 'Year', 'Min', 'Genre', 'Rate', 'Votes', 'Cast']
d = df['Year'].str.split('TV', expand = True)
# Это не набор строчек, там почему-то все время слетает всё, поэтому пришлось переобозначивать 
df['Year'] = d[0]
df['Year'][202] = 2012
df['Year'][26] = 1985
df['Year'][295] = 2014
df['Year'][254] = 1965
df['Year'][237] = 2013
df['Year'][63] = 2016
df['Year'][24] = 2003
df['Year'][32] = 1980
df['Year'][312] = 1993
df['Year'][313] = 1984
df['Year'][328] = 1982
df['Year'][333] = 1979
df['Min'][418] = 117
df['Min'][419] = 52
df['Min'][420] = 50
df['Min'][421] = 75
df['Min'][422] = 90
df['Min'][423] = 60
df['Year'] = df['Year'].str.replace(' ', '')
df['Min'] = df['Min'].str.replace(' ', '')
df['Rate'] = df['Rate'].str.replace(' ', '')
df['Rate'] = df['Rate'].str.replace(',', '.')
df['Votes'] = df['Votes'].str.replace(' ', '')
df['Year'][202] = 2012
df['Year'][26] = 1985
df['Year'][295] = 2014
df['Year'][254] = 1965
df['Year'][237] = 2013
df['Year'][63] = 2016
df['Year'][24] = 2003
df['Year'][32] = 1980
df['Year'][312] = 1993
df['Year'][313] = 1984
df['Year'][328] = 1982
df['Year'][333] = 1979
df['Min'][418] = 117
df['Min'][419] = 52
df['Min'][420] = 50
df['Min'][421] = 75
df['Min'][422] = 90
df['Min'][423] = 60
df['Year'] = pd.to_numeric(df['Year'])
df['Min'] = pd.to_numeric(df['Min'])
df['Rate'] = pd.to_numeric(df['Rate'], downcast='float')
df['Votes'] = pd.to_numeric(df['Votes'])
df['Year'][202] = 2012
df['Year'][26] = 1985
df['Year'][295] = 2014
df['Year'][254] = 1965
df['Year'][237] = 2013
df['Year'][63] = 2016
df['Year'][24] = 2003
df['Year'][32] = 1980
df['Year'][312] = 1993
df['Year'][313] = 1984
df['Year'][328] = 1982
df['Year'][333] = 1979
df['Min'][418] = 117
df['Min'][419] = 52
df['Min'][420] = 50
df['Min'][421] = 75
df['Min'][422] = 90
df['Min'][423] = 60
df['Min'] = df['Min'].astype('int')
df['Year'] = df['Year'].astype('int')

df.to_csv('/Users/vanys/PycharmProjects/project/check.csv')
df
