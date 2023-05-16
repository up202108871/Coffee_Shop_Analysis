import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title = "Coffee Shop Data Analysis", page_icon = '☕', layout="wide")

st.title('Coffee Shop Data Analysis')

st.subheader("State wise Sales:")
st.markdown('---')

@st.cache_data
def data_load():
    data = pd.read_csv('Coffee Chain.txt', sep="\t", encoding='utf-8', index_col = False)
    data_copy = data[['Area Code', 'Date', 'Market Size', 'Market',
                      'Product Line', 'Product Type', 'Product', 'Profit', 'Sales',
                      'State', 'Target Profit', 'Target Sales', 'Total Expenses', 'Type']]
    data_copy['Date'] = pd.to_datetime(data_copy['Date'])
    data_copy['DateNew'] = data_copy['Date'].dt.strftime("%Y-%m-%d")
    data_copy['Year'] = data_copy['Date'].dt.strftime('%Y')
    data_copy['Month'] = data_copy['Date'].dt.month_name()
    data_copy.drop(['Date'], axis=1, inplace=True)
    return data_copy

data = data_load()

data = data.groupby(["State", "Year"])[['Profit', 'Sales', 'Target Profit', 'Target Sales', 'Total Expenses']].sum()
data = data.reset_index()

data["StateCode"] = None
for ind, val in enumerate(data["State"]):
    if val == "Colorado":
        data["StateCode"].iloc[ind] = "CO"
    elif val == "Texas":
        data["StateCode"].iloc[ind] = "TX"
    elif val == "Florida":
        data["StateCode"].iloc[ind] = "FL"
    elif val == "Iowa":
        data["StateCode"].iloc[ind] = "IA"
    elif val == "Oklahoma":
        data["StateCode"].iloc[ind] = "OK"
    elif val == "Nevada":
        data["StateCode"].iloc[ind] = "NV"
    elif val == "Utah":
        data["StateCode"].iloc[ind] = "UT"
    elif val == "New Hampshire":
        data["StateCode"].iloc[ind] = "NH"
    elif val == "Louisiana":
        data["StateCode"].iloc[ind] = "LA"
    elif val == "Oregon":
        data["StateCode"].iloc[ind] = "OR"
    elif val == "Missouri":
        data["StateCode"].iloc[ind] = "MO"
    elif val == "Wisconsin":
        data["StateCode"].iloc[ind] = "WI"
    elif val == "Washington":
        data["StateCode"].iloc[ind] = "WA"
    elif val == "Massachusetts":
        data["StateCode"].iloc[ind] = "MA"
    elif val == "Illinois":
        data["StateCode"].iloc[ind] = "IL"
    elif val == "New Mexico":
        data["StateCode"].iloc[ind] = "NM"
    elif val == "Ohio":
        data["StateCode"].iloc[ind] = "OH"
    elif val == "New York":
        data["StateCode"].iloc[ind] = "NY"

data['Sales'] = data['Sales']
contain = st.container()
fig = px.choropleth(data,
                    locations='StateCode',
                    locationmode="USA-states",
                    scope="usa",
                    color='Sales',
                    color_continuous_scale="ylorbr",
                    width=1000,
                    height=500

                    )
st.plotly_chart(fig, use_container_width=True)