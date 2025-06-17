import pandas as pd

def monthly_summary(monthly_df:pd.DataFrame) -> dict:
    paid = monthly_df[monthly_df['Financial Status']=='paid']

    summary_df = paid.groupby("Billing Country").agg(
        count = ("Name", 'nunique'),
        total_HTVA = ("Price w/o Tax", 'sum'),
        total_TVA  = ("Tax 1 Value", 'sum'),
        total = ('Total', 'sum')
    ).sort_values("count", ascending=False)

    summary = {}
    
    summary['world'] = summary_df[summary_df['total_TVA'] == 0]
    summary['world'] = summary['world'].drop(["total_HTVA","total_TVA"], axis=1)
    summary['eu'] = summary_df[summary_df['total_TVA'] != 0]

    summary['eu'].loc['Total'] = summary['eu'].sum(numeric_only=True)
    summary['world'].loc['Total'] = summary['world'].sum(numeric_only=True)

    return summary