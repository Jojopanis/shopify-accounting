import pandas as pd

def split_countries(monthly_df:pd.DataFrame) -> dict:
    countries = set(monthly_df["Billing Country"].tolist())
    countries_df = {}
    for c in countries:
        countries_df[c] = monthly_df[monthly_df["Billing Country"]==c]
    return countries_df

def partially_refunded(country_df:pd.DataFrame):
    pass