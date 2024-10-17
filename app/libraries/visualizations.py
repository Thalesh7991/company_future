import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def sales_cumulatives(df):
    # Agrupar por Ano e Mês e calcular o faturamento mensal
    df_grouped = df.groupby(['Year', 'Month'])['TotalAmount'].sum().reset_index()

    # Ordenar por Ano e Mês para facilitar o cálculo acumulado
    df_grouped = df_grouped.sort_values(by=['Year', 'Month'])

    # Calcular o faturamento acumulado para cada ano
    df_grouped['CumulativeSales'] = df_grouped.groupby('Year')['TotalAmount'].cumsum()

    # Criar o gráfico de linhas com Plotly Express
    fig = px.line(
        df_grouped, 
        x='Month', 
        y='CumulativeSales', 
        color='Year', 
        title="Faturamento Acumulado por Ano",
        labels={'CumulativeSales': 'Faturamento Acumulado', 'Month': 'Mês'}
    )
    return fig
    


def sales_by_status(df):
    # Criar o gráfico de pizza
    fig = px.pie(df, 
                values='TotalAmount', 
                names='OrderStatus', 
                title='Distribuição de Vendas por Status',
                hole=0.3)  # Gráfico de donut
    return fig

def sales_by_method(df):
    df_count = df[['PaymentMethod', 'Unnamed: 0']].groupby('PaymentMethod').count().reset_index()

    # Gráfico horizontal por método de pagamento
    fig = go.Figure(go.Bar(
                x=df['Unnamed: 0'].to_list(),
                y=df['PaymentMethod'].to_list(),
                orientation='h'))
    
    return fig