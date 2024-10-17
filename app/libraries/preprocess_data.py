import pandas as pd

def preprocess_sales(df):
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['ShippedDate'] = pd.to_datetime(df['ShippedDate'])
    df['Year'] = df['OrderDate'].dt.year.astype(int)
    df['Month'] = df['OrderDate'].dt.month
    df = df.loc[df['Year'] >= 2018]
    return df


def pct_rank_qcut(series, n, tipo_analise):
    if tipo_analise == 'Recency':
        edges = pd.Series([float(i) / n for i in range(n + 1)])
        f = lambda x: (edges >= x).values.argmax()
        return series.rank(pct=1, ascending=0).apply(f)
    else:
        edges = pd.Series([float(i) / n for i in range(n + 1)])
        f = lambda x: (edges >= x).values.argmax()
        return series.rank(pct=1).apply(f)


# Define rfm_level function
def rfm_level(df):
    if df['R'] <= 2 and df['F'] <= 2.5:
        return 'Hibernando'
    elif (df['R'] <= 2 and df['F'] > 2.5 and df[
        'F'] <= 4.5):  # Clientes que ja tiveram uma frequencia alta, porém não compram faz muito tempo
        return 'Em Risco'
    elif (df['R'] <= 2 and df[
        'F'] > 4.5):  # Clientes que ja tiveram uma frequencia alta, porém não compram faz muito tempo
        return 'Prestes a Perder'
    elif (df['R'] > 2 and df['R'] <= 3.5 and df['F'] <= 2.5):
        return 'Prestes a Dormir'

    elif (df['R'] > 2.5 and df['R'] <= 3.5 and df['F'] > 2.5 and df['F'] <= 3.5):
        return 'Precisa de Atenção'

    elif (df['R'] > 2 and df['R'] < 5 and df['F'] > 3.5):
        return 'Clientes Fiéis'

    elif (df['R'] > 3.5 and df['R'] <= 4.5 and df['F'] <= 1.5):
        return 'Promissores'

    elif (df['R'] > 3.5 and df['F'] >= 1.5 and df['F'] <= 3.5):
        return 'Potentiais Clientes Fieis'
    elif (df['R'] >= 5 and df['F'] >= 3.5):
        return 'Champions'
    elif (df['R'] >= 5 and df['F'] <= 1.5):
        return 'Novos Clientes'
