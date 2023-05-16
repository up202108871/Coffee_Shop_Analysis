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

st.subheader("Data:")
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
    data_copy['MonthNumber'] = data_copy['Date'].dt.strftime('%m')
    data_copy['Month Year'] = data_copy['Date'].dt.strftime('%Y-%m')
    data_copy.drop(['Date'], axis=1, inplace=True)
    return data_copy

data = data_load()

values = ['Profit', 'Sales', 'Target Profit', 'Target Sales', 'Total Expenses']
variables = ['Market Size', 'Market', 'Product Line', 'Product Type', 'Product', 'State', 'Type']
year = data["Year"].unique()
segments = ['Market Size', 'Market', 'Product Line', 'Product Type', 'Product', 'State', 'Type']


line_data = data.groupby(["MonthNumber", "Month", "Year"])[['Profit', 'Sales', 'Target Profit', 'Target Sales', 'Total Expenses']].sum()
line_data = line_data.reset_index()
line_data = line_data.sort_values("MonthNumber")

with st.sidebar:
    st.write("Filters")

    year_value = st.multiselect("Years", year, default = year[-1])

    multi_val_line = st.checkbox("Add multiple lines")

    if multi_val_line:
        line_value = st.multiselect("Line Chart Values", values, default = "Sales")
        st.warning("Bar graph supports only single value. Choose value from below box to show in bar graph")
        bar_value = st.selectbox("Bar Graph Value", values, index=1)
    else:
        line_value = st.selectbox("Value", values, index=1)



    bar_variables = st.selectbox("Bar Graph Variable", segments, index=0)
    multi_val_bar = st.checkbox("Add segments to bars")

    if multi_val_bar:
        bar_segment = st.selectbox("Bars Segments", segments, index = 0)

line_data = line_data.query("Year == @year_value")

if multi_val_line:
    if len(line_value) == 1:
        title = f"{line_value[0]} over time."
    elif len(line_value) == 2:
        title = f"{line_value[0]} and {line_value[1]} over time."
    elif len(line_value) == 3:
        title = f"{line_value[0]},{line_value[1]} and {line_value[2]} over time."
    elif len(line_value) == 4:
        title = f"{line_value[0]},{line_value[1]}, {line_value[2]} and {line_value[3]} over time."
    else:
        title = f"{line_value[0]},{line_value[1]}, {line_value[2]}, {line_value[3]} and {line_value[4]} over time."
else:
    title = f"{line_value} over time."

emp, line_chart = st.columns([1,6])
with line_chart:
    line = px.line(line_data, x = "Month", y = line_value, title = title)
    st.plotly_chart(line)

bar_data = data.query("Year == @year_value")


if multi_val_line:
    if multi_val_bar:
        bar_title = f"{bar_value} over {bar_variables} distributed on {bar_segment}"
    else:
        bar_title = f"{bar_value} over {bar_variables}"
    st.warning("Bar graph supports only single value.")
    if multi_val_bar:
        bar = px.bar(bar_data, x = bar_variables, y = bar_value, color = bar_segment, title = bar_title)
    else:
        bar = px.bar(bar_data, x = bar_variables, y = bar_value, title = bar_title)
else:
    if multi_val_bar:
        bar_title = f"{line_value} over {bar_variables} distributed on {bar_segment}"
    else:
        bar_title = f"{line_value} over {bar_variables}"
    if multi_val_bar:
        bar = px.bar(bar_data, x = bar_variables, y = line_value, color = bar_segment, title = bar_title)
    else:
        bar = px.bar(bar_data, x = bar_variables, y = line_value, title = bar_title)

empty, bar_chart = st.columns([1,6])

with bar_chart:
    st.plotly_chart(bar)