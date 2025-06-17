import pandas as pd

pd.options.mode.copy_on_write = True

def keep_essential(df:pd.DataFrame) -> pd.DataFrame:
    df = df[["Name", "Paid at", "Financial Status", "Billing Country",  "Total", "Tax 1 Value", "Lineitem name", "Lineitem quantity", "Refunded Amount"]]
    df["Tax 1 Value"] = df["Tax 1 Value"].fillna(0)
    df["Total"] = df["Total"].fillna(0)
    df = df.ffill()
    df["Price w/o Tax"] = df["Total"] - df["Tax 1 Value"]
    df["Paid at"] = df["Paid at"].map(lambda x:x[:10])
    return df

def split_months(df:pd.DataFrame) -> dict:
    df = keep_essential(df)
    df['Month'] = df['Paid at'].map(lambda x:x[5:7])
    months = set(df["Month"].tolist())
    monthly_dfs = {}
    for m in months:
        monthly_dfs[m] = df[df['Month']==str(m)]
        monthly_dfs[m] = monthly_dfs[m].drop('Month', axis=1)
    return monthly_dfs