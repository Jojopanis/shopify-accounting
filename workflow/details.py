import pandas as pd

def add_credit(df:pd.DataFrame):
    df['tax_amount'] = round(df['total']/df['prix_HTVA'],2)
    df["tax_credit"] = round(df['refunded']-df['refunded']/df['tax_amount'],2)
    return df

def combine_orders(df:pd.DataFrame):
    df = df.groupby("Name").agg(
        date = ('Paid at', 'min'),
        prix_HTVA = ('Price w/o Tax', 'sum'),
        TVA = ('Tax 1 Value', 'sum'),
        total = ('Total', 'max'),
        number = ('Lineitem quantity', 'sum'),
        desc = ('Lineitem name', 'sum'),
        financial_status = ('Financial Status', 'first'),
        refunded = ('Refunded Amount', 'first'))
    add_credit(df)
    return df

def split_countries(monthly_df:pd.DataFrame) -> dict:
    countries = set(monthly_df["Billing Country"].tolist())
    countries_df = {}
    for c in countries:
        countries_df[c] = combine_orders(monthly_df[monthly_df["Billing Country"]==c])
    return countries_df

def paid_table(df:pd.DataFrame):
    isEU = True if df['TVA'].sum() != 0 else False
    if isEU:
        df=df[['date', 'prix_HTVA', 'TVA','total','number', 'desc']]
    else:
        df=df[['date','total','number','desc']]
    return df

def refund_table(df:pd.DataFrame):
    isEU = True if df['TVA'].sum() != 0 else False
    df=df[df['financial_status']!='paid']
    if isEU:
        df=df[['prix_HTVA', 'TVA','total','refunded', 'tax_credit']]
    else:
        df=df[['total','refunded']]

    if df.empty == True:
        df.loc['###'] = 0
    return df