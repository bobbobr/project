import pandas as pd
import numpy as np
import streamlit as st
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import folium
import geopandas as gpd
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit_folium
from streamlit_folium import st_folium
from sklearn.linear_model import LinearRegression
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt
import scipy.sparse as sp
import seaborn as sns


with st.echo(code_location='below'):

    st.title('Финальный проект. Анализ книг')
    st.header("Вначале проанализируем экранизацию известных книг, а затем посмотрим где можно купить бумажный вариант")
    st.subheader("Сперва возьмем данные с помощью продвинутого вебскрепинга с сайта IMBD и запишем их в csv, так как selenium в streamlit работает не так, как я хотел.")
    # Здесь начинаю визуализировать данные
    # Данные собраны через провдинутый вебскрепинг. Смотреть файл main.py
    s = pd.read_csv('check.csv')
    show_data = st.expander("Посмотреть данные")

    with show_data:
        st.write(s.head(20))
    p = s.groupby('Year').mean().reset_index()
    st.caption('Здесь можно посмотреть детально по годам')
    sel = st.selectbox("Параметр", p.columns[2::])
    if sel:
        fig1 = px.line(p, x = p['Year'], y = sel)
        st.plotly_chart(fig1)

    # Использую машинное обучение
    st.subheader('Затем хотелось бы научиться предсказывать, если фильм идет n минут, то какой у него будет рейтинг')
    model = LinearRegression()
    model.fit(s[["Min"]], s["Rate"])
    st.caption('Введите продолжительность в минутах')
    number=st.number_input('Insert a number.')
    st.subheader(min(10, model.predict(pd.DataFrame([[number]], columns=["Min"]))[0]))

    # Использую математический аппарат Python
    min_array = np.array(s[['Min']])
    rate_array = np.array(s[['Rate']])
    vote_array = np.array(s[['Votes']])
    year_array = np.array(s[['Year']])
    st.subheader('Затем хотелось бы посмотреть, а есть ли связь между другими параметрами')
    st.caption('Используя математические возможности, расчитаем коэффициет корреляции')
    st.markdown("Выберите 2 параметра для которого будем считать коэфициент корреляции.")
    name_ = st.multiselect("Параметр", ['Year','Min', 'Votes', 'Rate'])
    if len(name_)==2:
        st.write(np.corrcoef(np.array(s[name_[0]]),np.array(s[name_[1]])))
    fig, ax = plt.subplots()    
    sns.heatmap(pd.DataFrame.corr(s[['Min', 'Rate', 'Votes', 'Year']].dropna(), method='pearson'), annot=True, annot_kws={'fontsize':10}, vmin=-1, vmax=1, linewidth=1, cmap='icefire')
    st.pyplot(fig)


    st.header('После просмотра экранизации фильма, хотелось бы купить бумажную версию книги. Это можно сделать в Читай-городе. Давайте посмотрим, где они есть в Москве')

    # Данные собраны через недокументированные API. Смотреть файл data.py, где дополнительно использую регулярные выражения
    # Помимо этого использую дополнительные технологии в виде fakeuseragent. Для обхода блокировок сайта.
    l = pd.read_csv('data.csv')
    show_data = st.expander("Посмотреть данные")

    with show_data:
        st.write(l.head(20))
    # Работаю с геоданными и отоброжаю их на карте, используя продвинутые пандас
    gdf = gpd.GeoDataFrame(l, geometry=gpd.points_from_xy(l['lon'], l['lat']))

    #st.write(gdf)

    m = folium.Map([55.75364, 37.648280], zoom_start=10)
    for ind, row in gdf.iterrows():
        folium.Marker([row.lat, row.lon], radius=30, fill_color='red').add_to(m)
    st.write('В этих местах в Москве находится Читай-город')
    a=st_folium(m)

    # Дополняю визуализацию данных, работу с геоданными, и продвинутые пандас
    lol = pd.read_csv('moscow.csv')
    show_data = st.expander("Посмотреть данные")

    with show_data:
        st.write(lol.head(20))
    st.subheader('Посмотрим в каких районах больше всего Читай-города')
    lol['poly'] = gpd.GeoSeries.from_wkt(lol['poly'])
    lol = gpd.GeoDataFrame(lol, geometry = 'poly')
    l = gpd.GeoDataFrame(l, geometry = gpd.points_from_xy(l['lon'], l['lat']))
    gl = l.sjoin(lol, how="inner", predicate='intersects')
    loljson = lol.to_json()
    loljson = json.loads(loljson)

    tut = gl['name'].value_counts()
    itog = lol.set_index('name').assign(tut = tut)
    itog.crs = "EPSG:4326"
    itog = itog.fillna(0)
    itog = itog.reset_index()
    itog['tut'] = itog['tut'].astype(int)
    itog['name'] = itog['name'].astype(str)
    m1 = folium.Map([55.75364, 37.648280], zoom_start=10)

    sto = folium.Choropleth(geo_data=loljson, data=itog, columns=['name','tut'],
                      key_on = 'feature.properties.name',
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      legend_name='num',
                      highlight=True,
                      reset=True).add_to(m1)
    sto.geojson.add_child(folium.features.GeoJsonTooltip(['name'],labels=False))
    plo = st_folium(m1)

    # Использую графы. в файле data.py я сделал это через sql, но в streamlit проблемы с подключением к бд, поэтому тут я сделал по-другому, чтобы показать результат. Использование sql посмотрите в файле data.py. Спасибо
    st.subheader('Затем я хочу посмотреть на мою любимую книгу Гарри Поттер и кто из героев относится к какой школе. Это идеально показать через графы')
    mis = None
    lis = []
    with open('characters.json') as json_file:
        mis = json.load(json_file)
    df = pd.DataFrame(mis)
    df1 = df['name']
    df1 = pd.DataFrame(df1)
    df1['house'] = df['house']
    df1= df1.dropna()
    show_data = st.expander("Посмотреть данные")

    with show_data:
        st.write(df1.head(20))
    hs = []
    for i in range(len(df1.values)):
        hs.append((df1.values[i][0],df1.values[i][1]))
    we = nx.Graph(hs)
    nx.draw(we)
    fig, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(we,)
    st.subheader('Вы можете выбрать школу и затем вам покажут её членов')
    harry = st.selectbox('Выберите факультет', options = df1['house'].unique())
    nx.draw(we.subgraph([harry] + list(we.neighbors(harry))), pos, with_labels=True)
    st.pyplot(fig)
    
    '''
    Использованные технологии:
    * обработка данных с помощью pandas
    * сложные технологии веб-скреппинга (Selenium)
    * работа с недокументированным API
    * визуализация( по годам, две карты Москвы)
    * numpy(работа с массивами, преобразование данных, подсчет корреляции)
    * streamlit
    * SQL
    * регулярные выражения
    * работа с геоданными
    * машинное обучение
    * работа с графами
    * доп технологии: продвинутый парсинг с fakeuseragent 
    * больше 120 строк)
    
    Ссылка на гитхаб: https://github.com/bobbobr/project  для просмотра data.py и main.py, где код по сбору данных и другие использованные технологии
    '''

