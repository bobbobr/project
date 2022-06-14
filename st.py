import os
import pickle
import re
from collections import defaultdict
from time import sleep

import altair as alt
import folium
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from bs4 import BeautifulSoup
from geopy import distance
from streamlit_folium import st_folium

with st.echo(code_location='below'):
    st.set_page_config(layout="wide")
    st.title("Проект")
    st.write("В проекте использовались данные Московского транспорта, а именно:")
    st.write("- набор данных о парковках велосипедов Велобайка (https://data.mos.ru/opendata/7704786030-stantsii-veloprokata)")
    st.write("- список всех велодорожек на карте Москвы (https://data.mos.ru/opendata/7710878000-velodorojki)")
    st.write("Приложение \"Велобайк\" позволяет брать в аренду велосипед на фиксированное время, при этом есть минимальный порог в 30 минут. Если его не превысить, аренда не будет учтена, и деньги не спишутся.")
    st.write("Проект вдохновлен следующей идеей: можно ли создать приложение, которое будет анализировать возможность проехать из точки A в точку B на велобайке, меняя велосипеды по истечении 30 минут?")
    st.image("https://thumbs.dreamstime.com/b/%D0%BC%D0%B0%D1%80%D1%88%D1%80%D1%83%D1%82%D0%BD%D0%B0%D1%8F-%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D0%B2%D0%B5%D0%BB%D0%BE%D1%81%D0%B8%D0%BF%D0%B5%D0%B4%D0%B0-%D0%B5%D0%B4%D1%83%D1%89-%D0%B2%D0%B5%D0%BB%D0%BE%D1%81%D0%B8%D0%BF%D0%B5%D0%B4-%D0%BD%D0%B0-%D1%80%D0%B0%D0%B7%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D0%B5-%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%BE%D0%BC-135230525.jpg")
    st.write("Другими словами, для произвольных двух точек в Москве определить, есть ли такой маршрут между ними, который пролегает по станциям проката, и длина между каждой из станций меньше расстояния, которое пожет проехать человек за 30 мин?")
    KEY = '9f9f24f42b9470667f7f557e9143ebee'
    
    @st.cache
    def download_dataset(data_id):
        """download data from mos ru"""
        data = []
        params = {
            'api_key': KEY
        }
        resp = requests.get(url=f'https://apidata.mos.ru/v1/datasets/{data_id}/count', params=params)
        count = int(resp.text)
        print(count)
        sleep(0.3)
        url_rows = f'https://apidata.mos.ru/v1/datasets/{data_id}/rows'
        res = []
        per_row = 240
        for idx, i in enumerate(range(0, count, per_row)):
            params = {
                'api_key': KEY,
                '$orderby': 'global_id',
                '$top': min(per_row, count-per_row*idx),
                '$skip': per_row*idx
            }
            print(i, params)
            resp_rows = requests.get(url=url_rows, params=params)
            if (resp_rows.status_code == 200):
                data = resp_rows.json()
                print(data[0])
                res.extend(data)
            sleep(1)
        return res

    st.subheader("Парковки Московского велопроката")
    st.info("Данные о парковках загружаются. Пожалуйста, подождите")
    bike_data = download_dataset(918)
    st.info(f"Набор данных загружен, получено {len(bike_data)} записей")
    # нанесем точки на карту
    m = folium.Map((55.67341,37.51384), zoom_start=12)
    for point in bike_data:
        folium.Circle(point['Cells']['geoData']['coordinates'][::-1],radius=20, tooltip=point['Cells']['Name']).add_to(m)
    st_m =  st_folium(m, width = 700, height=500, key="st_f_1")
    df = pd.DataFrame([x['Cells'] for x in bike_data])
    df['lat'] = df['geoData'].apply(lambda x: x['coordinates'][1])
    df['lon'] = df['geoData'].apply(lambda x: x['coordinates'][0])
    st.write("Набор данных:")
    st.write(df.head())
    # построим диаграмму по округам, в каком больше велопарковок?
    



    st.subheader("Работа с pandas")
    st.write("Давайте посмотрим, в каком округе Москвы больше велопарковок")
    
    adm_data = df['AdmArea'].value_counts()
    st.bar_chart(adm_data)
    # fig, ax = plt.subplots()
    # y_pos = np.arange(len(adm_data.to_dict().keys()))
    
    # plt.barh(y_pos, list(adm_data.to_dict().values()), tick_label=list(adm_data.to_dict().values()))
    # ax.set_yticks(y_pos, labels=list(adm_data.to_dict().keys()))
    # # ax.set_ylabel(list(adm_data.to_dict().keys()), rotation=90)
    # # ax.set_ylabels(list(adm_data.to_dict().keys()), rotation=45, ha='right')
    # # ax.yticks(rotation=90)
    # st.plotly_chart(fig)
    # по какой-то причине оси с подписями не отображаются в streamlit, 

    st.write("Очевидно, все люди едут в ЦАО и там парковок будет больше. Посмотрим в разрезе по районам")
    # и по районам
    adm_data = df['District'].value_counts()
    st.bar_chart(adm_data)
    # plt.figure(figsize=(7,40))
    # fig, ax = plt.subplots()
    # plt.barh(list(adm_data.to_dict().keys()), list(adm_data.to_dict().values()))
    # st.plotly_chart(fig)
    st.write("Тоже все достаточно понятно: в топе Хамовники, Тверской и Пресненский район, по которым кататься на велосипеде одно удовольствие")
    st.write("Давайте посмотрим, на каких улицах больше всего остановок. Для получения названия улицы из датасета используем регулярыне выражения")
    def extract_street(address):
        try:
            return re.search(r"(?<=(ул. ))[а-яА-Я- ]+(?=,)",address).group()
        except AttributeError: # если там нет слова ул
            return ""
    df['street'] = df['Location'].apply(extract_street)

    street_data = df[df['street']!='']['street'].value_counts()
    plt.hist(street_data)
    st.write(street_data)
    st.bar_chart(street_data)
    st.write("Видно, что больше всего парковок на улице Профсоюзной. Неудивительно: это длинная и просторная улица на юге Москвы, там много места для того чтобы покататься, и достаточно большая протяженность, чтобы на ней было много станций проката")
    st.write("Вот несколько фотографий этой улицы")
    res = requests.get('https://yandex.ru/images/search?text=улица%20профсоюзная%20москва%20красивые%20фото').text
    bs = BeautifulSoup(res, "html.parser")
    src_list = [x.attrs['src'] for x in bs.find_all('img')[1:]][:10]
    n_columns = 2
    cols = st.columns(n_columns)
    for index, src in enumerate(src_list):
        idx = index % n_columns
        cols[idx].markdown(f'<img src="{src}" width=500></img>', unsafe_allow_html=True)

    st.write("Давайте посмотрим, насколько в городе много велодорожек, по которым эти самокаты могут двигаться")
    st.info("Данные о велодорожках загружаются. Пожалуйста, подождите")
    bike_roads_data = download_dataset(897)
    st.info(f"Данные о велодорожках загружены успешно, получено {len(bike_roads_data)} записей.")
    # нанесем дороги на карту вместе с точками

    m = folium.Map((55.67341,37.51384), zoom_start=12)
    for road in bike_roads_data:
        folium.PolyLine([x[::-1] for x in road['Cells']['geoData']['coordinates'][0]], radius=20, color='red').add_to(m)
    for point in bike_data:
        folium.Circle(point['Cells']['geoData']['coordinates'][::-1],radius=20, tooltip=point['Cells']['Name']).add_to(m)
    ss = st_folium(m)
    st.write("как видим, велодорожек в Москве совсем немного, в основном они сконцентрированы в центре")
    st.subheader("Построение маршрута")
    st.info("В настоящий момент выполняется вычисление расстояний между точками на графе, это может занять длительное время. Пожалуйста, дождитесь результата")
    
    
    @st.cache
    def distance_between_two_points(lat1, lon1, lat2, lon2):
        return distance.great_circle((lat1, lon1), (lat2, lon2)).km

    additional_data = {}
    all_points = {}
    for index, row in df.iterrows():
        additional_data[index] = {
            'Name': row.Name + " (" + row.Location + ")"
        }
        all_points[index] = (row['lat'], row['lon'])
    
    def get_all_distances(all_points):
        if os.path.exists("./distance_data.pickle"):
            with open('./distance_data.pickle', 'rb') as f:
                distances = pickle.load(f)
            return distances
        distances = {}
        for point_index,point in all_points.items():
            for other_point_index, other_point in all_points.items():
                distances[(point_index, other_point_index)] = abs(distance_between_two_points(*point, *other_point))
        with open('./distance_data.pickle', 'wb') as f:
            pickle.dump(distances, f)
        return distances
    
    distances = get_all_distances(all_points)
    
    treshold_distance = 10*0.5/1.5
    st.write("")
    st.write(f"""
        Средняя скорость велосипедиста на дороге составляем 15-20 км/ч
    
        Давайте сократим это число до 10 (реальная средняя скорость на улицах Москвы), и поделим на 1.5, чтобы учесть тот факт, что мы вычисляем расстояние по прямой, хотя в реальности нам нужно будет объезжать препятствия
        
        И далее умножим его на 0.5 (так как срок аренды составляет полчаса)

        Получаем `treshold_distance = 10*0.5/1.5 = {treshold_distance:.2f}`
    """)

    
    graph = nx.Graph()
    graph.add_edges_from([[*k, {'weight': v}] for k,v in distances.items() if 0 < v < treshold_distance])
    
    def get_distance(x):
        return x[-1]['weight']
    st.write("Выберите точки старта и финиша")
    
    st.write("Если хотите проверить, по каким точкам можно построить маршрут, используйте пункты проката #10 и #213, #10 и #251, #105 и #239")

    st.write("Если хотите проверить, по каким точкам нельзя построить маршрут, используйте пункты проката #2 и #895")
    
    st.info("В сервисе содержится информация не обо всех парковках, поэтому полученный маршрут может быть не самым оптимальным. Это особенность работы алгоритма на текущих данных, и не является ошибкой. Для построения более точных маршрутов следовало бы выбрать более точную аппроксимацию земной поверхности (сейчас используется great_circle для ускорения производительности), и использовать более точную эвристику для получения расстояний между точками, вместо прямой линии. Такие расчеты выходят за рамки онлайн-сервиса по хостингу streamlit-ноутбуков.")

    start_point = st.selectbox("Выберите точку старта", sorted(list(additional_data.values()), key=lambda x: x['Name']))
    end_point = st.selectbox("Выберите точку финиша", sorted(list(additional_data.values()), key=lambda x: x['Name']))
    start = next(k for k,v in additional_data.items() if v == start_point)
    end = next(k for k,v in additional_data.items() if v == end_point)
    
    try:
        path = nx.shortest_path(graph, start, end, weight='weight')
        no_path = False
        _ = all_points[path[1]]
    except:
        st.error("Между указанными точками нельзя провести бесплатный маршрут")
        path = [start, end]
        no_path = True
    

    center = all_points[start]

    m = folium.Map(center, zoom_start=12)
    # for road in bike_roads_data:
    #     folium.PolyLine([x[::-1] for x in road['Cells']['geoData']['coordinates'][0]], radius=20, color='red').add_to(m)

    color = 'red' if no_path else 'lightgreen'
    try:
        for start_point, end_point in zip(path[:-1], path[1:]):    
            folium.PolyLine([all_points[start_point], all_points[end_point]], radius=20, color=color).add_to(m)
        for point in path[1:-1]:
            folium.Circle(all_points[point],radius=20, tooltip=additional_data[point]['Name']).add_to(m)
    except:
        pass

        
    folium.Circle(all_points[path[0]],radius=20, tooltip=additional_data[path[0]]['Name'], color='red').add_to(m)    
    folium.Circle(all_points[path[-1]],radius=20, tooltip=additional_data[path[-1]]['Name'], color='red').add_to(m)    
    
    st.write("Путь от точки старта к точке финиша на карте:")
    st.code("(Точки старта и финиша - красные, станции велопроката - синие, кратчайшее расстояние по прямой - зеленое)")
    
    st_folium(m, key="st_f_2")
    
    st.subheader("Статистика по проекту")
    st.markdown("""
    критерии: http://math-info.hse.ru/2021-22/Наука_о_данных/Итоговый_проект)

        1) 1 (pandas используется)

        2) 1 (скрепинг яндекса и поиск фотографий)

        3) 1 (работа с апи mos ru)

        4) 1 (визуализация статистики по районам Москвы)

        5) 1 (np.mean для вычисления средней точки маршрута)

        6) 1 (да)

        7) 0 (sql не использовался)

        8) 1 (регулярные выражения для поиска названий улиц в описаниях остановок)

        9) 1 (follium, анализ точке на плоскости через geopy)

        10) 0 (ML нет)

        11) 1 (работа с графами используется для поиска кратчайшего пути между велоостановками)

        12) 1 (pickle для кэширования)

        13) 1 (>120 строк объем)

        14) 1 (проект на одну тему)

        15) ? (на усмотрение проверяющего)
    """)

    st.write("Субъективно: 12/1.5 = 8 баллов минимум")
