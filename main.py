import pandas as pd

from workflow.cleaning import split_months
from workflow.summary import monthly_summary
from workflow.details import split_countries

if __name__ == "__main__":
    df = pd.read_csv("orders_export (6).csv")
    months = split_months(df)
    print(split_countries(months["04"]).keys())