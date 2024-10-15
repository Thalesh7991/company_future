import pandas as pd

def preprocess_sales(df):
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['ShippedDate'] = pd.to_datetime(df['ShippedDate'])
    return df