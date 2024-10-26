# import sys
# import os

# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(ROOT_DIR)
# import datetime as dt
# import pandas as pd
# import streamlit as st
# import numpy as np
# import folium
# import plotly.graph_objects as go
# import plotly.express as px

# from libraries.preprocess_data import preprocess_sales, pct_rank_qcut, rfm_level

# # Setando o tamanho da página
# st.set_page_config( layout='wide' )

# # Leitura dos Dados
# df_raw = pd.read_csv('data/data.csv', encoding='unicode_escape')
# # df_raw = df_raw.drop('Unnamed: 8',axis=1)



# # Dropando Clientes com código NA
# df_raw = df_raw.dropna(subset=['CustomerID'])

# #Change Data Type
# df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'])


# #Data Filtering
# # Quantidade Negativa
# df2 = df_raw.loc[df_raw['Quantity'] > 0]


# # stock_code
# df2 = df2[~df2['StockCode'].isin( ['POST', 'D', 'DOT', 'M', 'S', 'AMAZONFEE', 'm', 'DCGSSBOY', 'DCGSSGIRL', 'PADS', 'B', 'CRUK'] ) ]

# #Bad User
# df2 =  df2.loc[~df2['CustomerID'].isin([16446])]

# ##### FEATURE ENGINEERING #####
# df3 = df2.copy()


# df_ref = df3.drop(['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice','Country'],axis=1).drop_duplicates( ignore_index=True )

# #faturamento
# df3['faturamento'] = df3['Quantity'] * df3['UnitPrice']
# df_monetary = df3[['CustomerID', 'faturamento']].groupby('CustomerID').sum().reset_index()
# df_ref = pd.merge(df_ref, df_monetary, how='left', on='CustomerID')


# #recencia
# df_recency = df3[['CustomerID', 'InvoiceDate']].groupby('CustomerID').max().reset_index()
# df_recency['recency_days'] = (df3['InvoiceDate'].max() - df_recency['InvoiceDate']).dt.days
# df_recency = df_recency[['CustomerID','recency_days']].copy()
# df_ref = pd.merge(df_ref, df_recency, how='left', on='CustomerID')

# #frequencia
# df_aux = ( df3[['CustomerID', 'InvoiceNo', 'InvoiceDate']].drop_duplicates()
#                                                              .groupby( 'CustomerID')
#                                                              .agg( max_ = ( 'InvoiceDate', 'max' ),
#                                                                    min_ = ( 'InvoiceDate', 'min' ),
#                                                                    days_= ( 'InvoiceDate', lambda x: ( ( x.max() - x.min() ).days ) + 1 ),
#                                                                    buy_ = ( 'InvoiceNo', 'count' ) ) ).reset_index()
# # Frequency
# df_aux['frequency'] = df_aux[['buy_', 'days_']].apply( lambda x: x['buy_'] / x['days_'] if  x['days_'] != 0 else 0, axis=1 )

# # Merge
# df_ref = pd.merge( df_ref, df_aux[['CustomerID', 'frequency']], on='CustomerID', how='left' )


# # rankeando cada atributo
# df_ref['R'] = pct_rank_qcut(df_ref['recency_days'],5, 'Recency')
# df_ref['F'] = pct_rank_qcut(df_ref['frequency'],5, 'Frequency')
# df_ref['M'] = pct_rank_qcut(df_ref['faturamento'],5, 'Monetary')

# # Aplicando SEGMENTAÇÃO DOS CLIENTES
# df_ref['segmentation'] = df_ref.apply(rfm_level, axis=1 )


# with st.sidebar:
#     st.title('FILTROS')


#     fat_min = df_ref['faturamento'].min()
#     fat_max = df_ref['faturamento'].max()
#     fat_mean = float(df_ref['faturamento'].mean())

#     rec_min = df_ref['recency_days'].min()
#     rec_max = df_ref['recency_days'].max()
#     rec_mean = float(df_ref['recency_days'].mean())

#     freq_min = df_ref['frequency'].min()
#     freq_max = df_ref['frequency'].max()
#     freq_mean = float(df_ref['frequency'].mean())




#     #Filtro de Grupo
#     groups_list = df_ref['segmentation'].drop_duplicates()
#     group_filter = st.multiselect('Grupo', groups_list)
#     if group_filter:
#         group_filter = group_filter
#     else:
#         group_filter = groups_list

#     #Filtro de Cliente
#     customers_list = df_ref['CustomerID'].drop_duplicates()
#     customer_filter = st.multiselect('Cliente', customers_list)
#     if customer_filter:
#         customer_filter = customer_filter
#     else:
#         customer_filter = customers_list

#     # Filtro de R Score
#     r_list = df_ref['R'].drop_duplicates()
#     r_score_filter = st.multiselect('Recency Score', r_list)
#     if r_score_filter:
#         r_score_filter = r_score_filter
#     else:
#         r_score_filter = r_list

#     # Filtro de Frequency Score
#     f_list = df_ref['F'].drop_duplicates()
#     f_score_filter = st.multiselect('Frequency Score', f_list)
#     if f_score_filter:
#         f_score_filter = f_score_filter
#     else:
#         f_score_filter = f_list

#     # Filtro de Monetary Score
#     m_list = df_ref['M'].drop_duplicates()
#     m_score_filter = st.multiselect('Score', m_list)
#     if m_score_filter:
#         m_score_filter = m_score_filter
#     else:
#         m_score_filter = m_list

#     #Filtro de faturamento
#     fat_slider = st.slider('Faturamento', min_value= float(fat_min), max_value= float(fat_max), step=1.0, value=float(fat_max) )



#     # Filtro de Recência
#     rec_slider = st.slider('Recência', min_value= float(rec_min), max_value= float(rec_max), step=1.0, value=float(rec_max) )

#     # Filtro de Frequência
#     freq_slider = st.slider('Frequência', min_value= float(freq_min), max_value= float(freq_max), step=1.0, value=float(freq_max) )


# st.title("Comportamento de Compra dos Clientes")

# df_ref = df_ref.loc[(df_ref['CustomerID'].isin(customer_filter)
#                      & df_ref['segmentation'].isin(group_filter)
#                      & df_ref['R'].isin(r_score_filter)
#                      & df_ref['F'].isin(f_score_filter)
#                      & df_ref['M'].isin(m_score_filter)
#                      & (df_ref['faturamento'] <= fat_slider)
#                      & (df_ref['recency_days'] <= rec_slider)
#                      & (df_ref['frequency'] <= freq_slider)

#                      )]

# # Pefil dos Grupos
# df_segmentation = df_ref[['CustomerID','segmentation']].groupby('segmentation').count().reset_index()
# df_segmentation['perc_customer'] = (df_segmentation['CustomerID'] / df_segmentation['CustomerID'].sum() )*100
# df_fat = df_ref[['segmentation','faturamento']].groupby('segmentation').mean().reset_index()
# df_segmentation =  pd.merge(df_segmentation, df_fat, on='segmentation', how='left')
# df_rec = df_ref[['segmentation','recency_days']].groupby('segmentation').mean().reset_index()
# df_segmentation =  pd.merge(df_segmentation, df_rec, on='segmentation', how='left')
# df_freq = df_ref[['segmentation','frequency']].groupby('segmentation').mean().reset_index()
# df_segmentation =  pd.merge(df_segmentation, df_freq, on='segmentation', how='left')
# df_segmentation.sort_values('faturamento', ascending=False)

# new_columns = ['Grupo', 'Qtde Clientes', '% de Clientes', 'Faturamento', 'Recência', 'Frequência']
# df_segmentation.columns = new_columns


# c1, c2 = st.columns(2)
# c1.header('Clientes por Grupo')

# #with c1:
# # Bar chart Customer per Segmentation
# customer_per_group = df_ref[['CustomerID', 'segmentation']].groupby(
#     'segmentation').count().reset_index().sort_values('CustomerID', ascending=0)
# fig = px.bar(customer_per_group, x='segmentation', y='CustomerID',
#                 labels={
#                     "segmentation": "Grupos",
#                     "CustomerID": "Qtde Clientes"
#                 }
#              )
# c1.plotly_chart(fig,width=50)

# #with c2:
# # Bar chart Faturamento per Segmentation
# c2.header('Faturamento Médio')
# faturamento_per_group = df_ref[['segmentation', 'faturamento']].groupby(
#     'segmentation').mean().reset_index().sort_values('faturamento', ascending=0)
# fig2 = px.bar(faturamento_per_group, x='segmentation', y='faturamento',
#                 labels={
#                     "segmentation": "Grupos",
#                     "faturamento": "Faturamento Médio (R$)"
#                 }
#               )
# c2.plotly_chart(fig2,use_container_width=True)


# c1, c2 = st.columns(2)
# # Bar chart recency per Segmentation
# c1.header('Tempo Médio Sem Compra (Dias)')
# recencia_per_group = df_ref[['segmentation', 'recency_days']].groupby(
#     'segmentation').mean().reset_index().sort_values('recency_days', ascending=0)
# fig3 = px.bar(recencia_per_group, x='segmentation', y='recency_days',
#                 labels={
#                     "segmentation": "Grupos",
#                     "recency_days": "Tempo Sem Comprar"
#                 }

#               )
# c1.plotly_chart(fig3, use_container_width=True)

# c2.header('Frequência de Compra')
# frequencia_per_group = df_ref.loc[(df_ref['faturamento'] <= fat_slider)
#                                    & (df_ref['recency_days'] <= rec_slider)
#                                    & (df_ref['frequency'] <= freq_slider)
#                                    & (df_ref['CustomerID'].isin(customer_filter))
#                                    & (df_ref['segmentation'].isin(group_filter))][['segmentation', 'frequency']].groupby(
#     'segmentation').mean().reset_index().sort_values('frequency', ascending=0)
# fig4 = px.bar(frequencia_per_group, x='segmentation', y='frequency',
#                 labels={
#                     "segmentation": "Grupos",
#                     "frequency": "Frequência"
#                 }
#               )
# c2.plotly_chart(fig4,use_container_width=True)




# # Linha Temporal Faturamento Médio por Mês
# #print(df_raw.columns)
# df3['TotalFat'] = df3['UnitPrice'] * df3['Quantity']
# df3 = pd.merge(df3, df_ref, on='CustomerID', how='left')
# #df3 = df3.loc[ (df3['segmentation'].isin(group_filter))]
# df_fat = df3.loc[(  df3['segmentation'].isin(group_filter) )

#                 ][['TotalFat', 'InvoiceDate']]

# st.header("Faturamento Mensal")

# fig5 = px.line(df_fat.groupby(pd.Grouper(key='InvoiceDate', axis=0, freq='M')).sum().reset_index(), x='InvoiceDate', y='TotalFat',
#                 labels={
#                     "InvoiceDate": "Meses",
#                     "TotalFat": "Faturamento"
#                 }
#                )
# st.plotly_chart(fig5,use_container_width=True,
#                 )
# #st.dataframe(df_fat.groupby(pd.Grouper(key='InvoiceDate', axis=0, freq='M')).sum().reset_index())


# df_filtered = df_ref.loc[ (df_ref['faturamento'] <= fat_slider)
#                                    & (df_ref['recency_days'] <= rec_slider)
#                                    & (df_ref['frequency'] <= freq_slider)
#                                    & (df_ref['CustomerID'].isin(customer_filter))
#                                    & (df_ref['segmentation'].isin(group_filter))
#                                    & (df_ref['R'].isin(r_score_filter))
#                                    & (df_ref['F'].isin(f_score_filter))
#                                    & (df_ref['M'].isin(m_score_filter))
#                                  ]



# ################################################### COHORT ############################################################

# def get_dates(df, column):
#     year = df[column].dt.year
#     month = df[column].dt.month
#     day = df[column].dt.day
#     return year, month, day

# # Função para obter o primeiro dia do mês
# def get_month(x):
#     return dt.datetime(x.year, x.month, 1)

# # Carregar o dataset (você pode carregar seu dataset aqui)
# # df = pd.read_csv("seu_dataset.csv")

# # Simulando um dataframe de exemplo
# # df = pd.DataFrame({
# #     "CustomerID": np.random.randint(1000, 2000, 1000),
# #     "InvoiceDate": pd.date_range(start='2021-01-01', periods=1000, freq='D')
# # })

# df = df_raw.copy()

# # Converter InvoiceDate para datetime
# df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# # Aplica a função para criar a coluna InvoiceMonth
# df["InvoiceMonth"] = df["InvoiceDate"].apply(get_month)

# # Calcula o CohortMonth (mês da primeira compra)
# df["CohortMonth"] = df.groupby("CustomerID")["InvoiceMonth"].transform("min")

# # Obtém os componentes de data
# invoice_year, invoice_month, invoice_day = get_dates(df, "InvoiceMonth")
# cohort_year, cohort_month, cohort_day = get_dates(df, "CohortMonth")

# # Calcula as diferenças entre anos e meses
# year_diff = invoice_year - cohort_year
# month_diff = invoice_month - cohort_month

# # Calcula o CohortIndex
# df["CohortIndex"] = 12 * year_diff + month_diff + 1

# # Agrupamento para calcular o tamanho de cada coorte
# cohort_data = df.groupby(["CohortIndex", "CohortMonth"])["CustomerID"].nunique().reset_index()

# # Pivot da tabela para visualização da coorte
# cohort_pivot = cohort_data.pivot(index="CohortMonth", columns="CohortIndex", values="CustomerID")

# # Tamanho da coorte
# cohort_sizes = cohort_pivot.iloc[:, 0]

# # Calcula a taxa de retenção
# retention = cohort_pivot.divide(cohort_sizes, axis=0)

# # Ajusta o índice para formato de ano e mês
# retention.index = retention.index.strftime("%Y-%m")

# # Título do Dashboard
# st.title("Cohort Analysis Dashboard")

# # Heatmap interativo com Plotly Express
# fig = px.imshow(retention, 
#                 labels=dict(x="Cohort Index", y="Cohort Month", color="Retention Rate"), 
#                 x=retention.columns, 
#                 y=retention.index, 
#                 color_continuous_scale="Blues", 
#                 aspect="auto",
#                 text_auto=".2%")

# # Exibe o gráfico no Streamlit
# st.plotly_chart(fig)









# st.header("Relatório de Clientes")
# df_filtered.columns = ['Cod Cliente', 'Faturamento', 'Recência (dias)', 'Frequência', 'R', 'F', 'M', 'Grupo']
# st.dataframe(df_filtered.sort_values('Faturamento', ascending=0 ))


