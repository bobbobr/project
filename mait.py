import pandas as pd
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
import streamlit_folium as st_folium



s = pd.read_csv('check.csv')
st.write(s)

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

url = 'https://www.chitai-gorod.ru/shops/'
params = {'format': 'json'}
r = requests.get(url, params, headers=header)
s = r.text
soup = BeautifulSoup(s, "html.parser")
ps = soup.find_all(class_='shop-list__item js__shop-list-item')
lat = []
lon = []
for i in range(len(ps)):
    lat.append(ps[i]['data-lat'])
    lon.append(ps[i]['data-lng'])
st.write(lat,lon)
l = pd.DataFrame({'lat':lat,'lon':lon})

gdf = gpd.GeoDataFrame(l, geometry=gpd.points_from_xy(l['lon'], l['lat']))
st.write(gdf)

m = folium.Map([55.75364, 37.648280], zoom_start=10)
for ind, row in gdf.iterrows():
    folium.Marker([row.lat, row.lon], radius=30, fill_color='red').add_to(m)

a=st_folium(m)
