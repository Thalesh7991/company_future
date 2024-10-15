import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from libraries.preprocess_data import preprocess_sales
from libraries.visualizations import sales_by_month, sales_by_country, sales_by_status

from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Configurar a página
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Título do dashboard
st.title('Acompanhamento de Vendas')

df = pd.read_csv('data/order.csv')
df = preprocess_sales(df)

# Organizar layout das colunas
left_column, right_column = st.columns(2)
left_column.plotly_chart(sales_by_month(df))
right_column.plotly_chart(sales_by_country(df))

left_column, right_column = st.columns(2)
left_column.plotly_chart(sales_by_status(df))


fig = go.Figure(go.Bar(
            x=df['TotalAmount'].to_list(),
            y=df['PaymentMethod'].to_list(),
            orientation='h'))
right_column.plotly_chart(fig)

df_loc = pd.read_csv('data/dados_lat.csv')


map_center = [df_loc['Latitude'].mean(), df_loc['Longitude'].mean()]  # Centralizar o mapa
mymap = folium.Map(location=map_center, zoom_start=10)

# Adicionar marcadores para cada endereço
for idx, row in df_loc.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Endereço: {row['Address']}<br>Vendas: ${row['Total Sales']}",
        tooltip=row['Address']
    ).add_to(mymap)

st.header("Vendas por Endereço")
# left_column, right_column = st.columns(2)
# with left_column:
folium_static(mymap,width=1400, height=500)

# st.dataframe(df)





