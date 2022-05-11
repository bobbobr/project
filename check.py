import streamlit as st
import pandas as pd
import numpy as np
import opendatasets as od
import requests

import pandas as pd

url = "https://raw.githubusercontent.com/rallen2lk/new-york-city-airport-activity/main/nyc-flights.csv"
c = pd.read_csv(url)
st.write(c)

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



def print_hello(name='Anna'):

    st.write(f"## Hello, {name}!")  # Press Ctrl+F8 to toggle the breakpoint.

print_hello()


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
   # print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
