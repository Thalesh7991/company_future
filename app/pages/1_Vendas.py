import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px

from libraries.preprocess_data import preprocess_sales
from libraries.visualizations import sales_by_month, sales_by_country, sales_by_status, sales_cumulatives, sales_by_method
import numpy as np
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Configurar a página
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")



# Carregar dados
df = pd.read_csv('data/order.csv')
df = preprocess_sales(df)

# Filtros no sidebar
st.sidebar.header("Filtrar Dados")

# Filtro por Data do Pedido (OrderDate)
min_date = pd.to_datetime(df['OrderDate']).min()
max_date = pd.to_datetime(df['OrderDate']).max()
date_range = st.sidebar.date_input("Período do Pedido", [min_date, max_date])

anos_disponiveis = np.sort(df['Year'].unique())
anos_selecionados = st.sidebar.multiselect('Selecione o(s) Ano(s)', options=anos_disponiveis, default=anos_disponiveis)

# Filtro por Status do Pedido (OrderStatus)
status_options = df['OrderStatus'].unique()
selected_status = st.sidebar.multiselect('Status do Pedido', status_options)

# Filtro por País (ShipCountry)
country_options = df['ShipCountry'].unique()
selected_country = st.sidebar.multiselect('País de Destino', country_options)

# Filtro por Método de Pagamento (PaymentMethod)
payment_options = df['PaymentMethod'].unique()
selected_payment_method = st.sidebar.multiselect('Método de Pagamento', payment_options)

# Filtro por Faixa de Valor Total (TotalAmount)
min_total = int(df['TotalAmount'].min())
max_total = int(df['TotalAmount'].max())
selected_total_range = st.sidebar.slider('Faixa de Valor Total (TotalAmount)', min_value=min_total, max_value=max_total, value=(min_total, max_total))

# Verificar se filtros estão vazios e aplicar os valores completos por padrão
if not selected_status:
    selected_status = status_options  # Usar todos os status se nada for selecionado

if not selected_country:
    selected_country = country_options  # Usar todos os países se nada for selecionado

if not selected_payment_method:
    selected_payment_method = payment_options  # Usar todos os métodos de pagamento se nada for selecionado


# Título do dashboard
st.title('Acompanhamento de Vendas')

# Aplicar os filtros ao DataFrame
filtered_df = df[
    (pd.to_datetime(df['OrderDate']).between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
    (df['OrderStatus'].isin(selected_status)) &
    (df['ShipCountry'].isin(selected_country)) &
    (df['PaymentMethod'].isin(selected_payment_method)) &
    (df['TotalAmount'].between(selected_total_range[0], selected_total_range[1])) &
    (df['Year'].isin(anos_selecionados))
]

faturamento = filtered_df['TotalAmount'].sum()
faturamento = "R$ {:,.2f}".format(faturamento).replace(",", "X").replace(".", ",").replace("X", ".")

quantidade_clientes = len(filtered_df['CustomerID'].unique())

ticket_medio = filtered_df['TotalAmount'].mean()
ticket_medio = "R$ {:,.2f}".format(ticket_medio).replace(",", "X").replace(".", ",").replace("X", ".")
# st.metric(value=faturamento, label='Faturamento')


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Faturamento:")
    st.subheader(faturamento)
with middle_column:
    st.subheader("Quantidade de Clientes:")
    st.subheader(f"{quantidade_clientes} Clientes")

with right_column:
    st.subheader("Ticket Médio:")
    st.subheader(ticket_medio)

# Organizar layout das colunas
left_column, right_column = st.columns(2)
left_column.plotly_chart(sales_by_month(filtered_df))
right_column.plotly_chart(sales_by_country(filtered_df))

left_column, right_column = st.columns(2)
left_column.plotly_chart(sales_by_status(filtered_df))


st.plotly_chart(sales_cumulatives(filtered_df))


right_column.plotly_chart(sales_by_method(filtered_df))

# Carregar dados de localização
df_loc = pd.read_csv('data/dados_lat.csv')

# Criar mapa com folium
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
folium_static(mymap, width=1400, height=500)

# Exibir tabela com os dados filtrados
st.dataframe(filtered_df)
