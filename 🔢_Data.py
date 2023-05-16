import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title = "Coffee Shop Data Analysis", page_icon = '☕', layout="wide")

st.title('Coffee Shop Data Analysis')

st.subheader("Data:")
st.markdown('---')

@st.cache_data
def data_load():
    data = pd.read_csv('Coffee Chain.txt', sep="\t", encoding='utf-8', index_col = False)
    data_copy = data[['Area Code', 'Date', 'Market Size', 'Market',
                      'Product Line', 'Product Type', 'Product', 'Profit', 'Sales',
                      'State', 'Target Profit', 'Target Sales', 'Total Expenses', 'Type']]
    data_copy['Date'] = pd.to_datetime(data_copy['Date'])
    data_copy['DateNew'] = data_copy['Date'].dt.strftime('%Y-%m-%d')
    data_copy['Year'] = data_copy['Date'].dt.strftime('%Y')
    data_copy['Month'] = data_copy['Date'].dt.month_name()
    data_copy['Month Year'] = data_copy['Date'].dt.strftime('%Y-%m')
    data_copy.drop(['Date'], axis=1, inplace=True)
    return data_copy

data = data_load()


st.dataframe(data)

