import pandas as pd

def read_csv(csv_path):
    file = pd.read_csv(csv_path)
    return file

def check_str_contains(df, column, str):
    df_mask = df[column].astype('str').str.contains(str)
    result = df[df_mask]
    return result