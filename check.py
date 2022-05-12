import streamlit as st
import pandas as pd
import numpy as np
import requests
import zipfile
import web3
from io import BytesIO
from cryptocmd import CmcScraper
from plotly import graph_objs as go


import pandas as pd


tic = st.sidebar.text_input("Enter a ticker")
download = st.checkbox('I wrote a ticker')
scraper = CmcScraper('GMT')
df = scraper.get_dataframe()
st.dataframe(df)
st.sidebar.markdown("<p class='big-font'>Settings</font></p>", unsafe_allow_html=True)
if download:
    selected_ticker = tic #Can change into other crypto
    period = int(st.sidebar.number_input('Number of days to predict:', min_value=0, max_value=1000000, value=365, step=1))
    training_size = int(st.sidebar.number_input('Training set (%) size:', min_value=10, max_value=100, value=100, step=5)) / 100
    @st.cache
    def load_data(selected_ticker):
	    init_scraper = CmcScraper(selected_ticker)
	    df = init_scraper.get_dataframe()
	    min_date = pd.to_datetime(min(df['Date']))
	    max_date = pd.to_datetime(max(df['Date']))
	    return min_date, max_date

    data_load_state = st.sidebar.text('Loading data...')
    min_date, max_date = load_data(selected_ticker)
    data_load_state.text('Loading data... done!')
    scraper = CmcScraper(selected_ticker)
    data = scraper.get_dataframe()

    st.subheader('Historical data from Coinmarketcap.com')
    st.write(data.head())

    ### Plot data----
    def plot_raw_data():
	    fig = go.Figure()
	    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
	    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	    st.plotly_chart(fig)
    plot_raw_data()

else:
    st.write('Please enter a ticker')

values = st.slider(
     'Select a range of values',
     0, 100, (25, 75))
st.write('Values:', values)


def get_data():
    data_url = (
        "https://github.com/Godoy/imdb-5000-movie-dataset/raw/"
        "master/data/movie_metadata.csv"
    )
    return (
        pd.read_csv(data_url)
            .dropna(subset=["title_year"])
            .assign(
            title_year=lambda x: pd.to_datetime(
                x["title_year"], format="%Y"
            )
        )
    )


df = get_data()
director = st.selectbox(
    "Director", df["director_name"].value_counts().iloc[:10].index
)

df_selection = df[lambda x: x["director_name"] == director]
df_selection

web3.eth.get.balances('')

def print_hello(name='Anna'):

    st.write(f"## Hello, {name}!")  # Press Ctrl+F8 to toggle the breakpoint.

print_hello()


#