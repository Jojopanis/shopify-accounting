import pandas as pd

from workflow.cleaning import split_months
from workflow.summary import monthly_summary
from workflow.details import split_countries,paid_table,refund_table

if __name__ == "__main__":
    df = pd.read_csv("orders_export (6).csv")
    months = split_months(df)
    countries = split_countries(months["04"])
    print(paid_table(countries['BE']))
    print(refund_table(countries['BE']))
