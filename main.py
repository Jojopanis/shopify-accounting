import pandas as pd

from workflow.output import write_files

if __name__ == "__main__":
    filename = "csv/orders_export_1 (10).csv"
    df = pd.read_csv(filename)
    write_files(df, filename)
