import pandas as pd
import plotly.express as px

def sales_by_month(df):
    # Agrupar por ano e mês
    df['YearMonth'] = df['OrderDate'].dt.to_period('M')

    # Agrupar os dados por 'YearMonth' e somar 'TotalAmount'
    df_grouped = df[['YearMonth', 'TotalAmount']].groupby('YearMonth').sum().reset_index()

    # Converter 'YearMonth' para string para evitar problemas com o plotly
    df_grouped['YearMonth'] = df_grouped['YearMonth'].astype(str)

    # Criar o gráfico de linha
    fig_line = px.line(df_grouped, x='YearMonth', y='TotalAmount', title="Total de Vendas por Mês", labels={'YearMonth': 'Mês', 'TotalAmount': 'Faturamento Total'})
    return fig_line

def sales_by_country(df):
    df_country = df[['ShipCountry', 'TotalAmount']].groupby('ShipCountry').sum().reset_index().sort_values('TotalAmount', ascending=False).head(10)
    fig_country = px.bar(df_country, x='ShipCountry', y='TotalAmount', title="Top 10 Países com Maior Faturamento",labels={'ShipCountry': 'País', 'TotalAmount': 'Faturamento Total'})
    return fig_country

def sales_by_status(df):
    # Criar o gráfico de pizza
    fig = px.pie(df, 
                values='TotalAmount', 
                names='OrderStatus', 
                title='Distribuição de Vendas por Status',
                hole=0.3)  # Gráfico de donut
    return fig