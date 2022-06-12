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
import plotly as plt


s = pd.read_csv('check.csv')
p = s.groupby('Year').mean().reset_index()
sel = st.selectbox("Параметр", p.columns[2::])
fig = px.line(p, x = p['Year'], y = sel)
st.plotly_chart(fig)

model = LinearRegression()
model.fit(s[["Min"]], s["Rate"])

number=st.number_input('Insert a number.')
st.subheader(model.predict(pd.DataFrame([[number]], columns=["Min"]))[0])

min_array = np.array(s[['Min']])
rate_array = np.array(s[['Rate']])
vote_array = np.array(s[['Votes']])
year_array = np.array(s[['Year']])
st.markdown("Выберите параметр для которого будем считать коэфициент корреляции.")
name_ = st.multiselect("Параметр", ['Year','Min', 'Votes', 'Rate'])
st.write(np.corrcoef(np.array(s[name_[0]]),np.array(s[name_[1]])))





l = pd.read_csv('data.csv')

gdf = gpd.GeoDataFrame(l, geometry=gpd.points_from_xy(l['lon'], l['lat']))

st.write(gdf)

m = folium.Map([55.75364, 37.648280], zoom_start=10)
for ind, row in gdf.iterrows():
    folium.Marker([row.lat, row.lon], radius=30, fill_color='red').add_to(m)

a=st_folium(m)

lol = pd.read_csv('moscow.csv')
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

mis = None
lis = []
with open('characters.json') as json_file:
    mis = json.load(json_file)
df = pd.DataFrame(mis)
df1 = df['name']
df1 = pd.DataFrame(df1)
df1['house'] = df['house']
df1= df1.dropna()
df1
we = nx.Graph([(frm,to) for (frm, to) in df1.values])

g4.from_nx(we)

