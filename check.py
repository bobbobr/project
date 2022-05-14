import streamlit as st
import pandas as pd
import plotly.express as px
from cryptocmd import CmcScraper
from plotly import graph_objs as go

with st.echo(code_location='below'):
    tic = st.text_input("Enter a ticker")
    download = st.checkbox('I wrote a ticker')
    if download:
        selected_ticker = tic
        @st.cache
        ### FROM: (https://github.com/sfwong46/streamlit-crypto-demo/blob/main/streamlit-crypto-demo.py)
        def load_data(selected_ticker):
            init_scraper = CmcScraper(selected_ticker)
            df = init_scraper.get_dataframe()
            min_date = pd.to_datetime(min(df['Date']))
            max_date = pd.to_datetime(max(df['Date']))
            return (min_date, max_date)


        data_load_state = st.sidebar.text('Starting load data...')
        min_date, max_date = load_data(selected_ticker)
        data_load_state.text('Done!')
        scraper = CmcScraper(selected_ticker)
        data = scraper.get_dataframe()

        st.subheader('Historical data from Coinmarketcap.com')
        st.write(data.head())


        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
            fig.layout.update(title_text='Price of selected ticker', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
        plot_raw_data()
        ### END FROM

    

    else:
        st.write('Please enter a ticker')

    projects = ['BTC', "GMT", 'SAND', 'APE', 'ZIL']
    ### FROM: (https://discuss.streamlit.io/t/checkbox-to-download-some-data-and-trigger-button/4160/4)
    tip = [st.sidebar.checkbox(project, key = project) for project in projects]
    save =  [project for project, checked in zip(projects, tip) if checked]
    ### END FROM

    if st.button('Download data'):
        for project in save:
            scraper = CmcScraper(project)
            data = scraper.get_dataframe()
            plot_raw_data()


