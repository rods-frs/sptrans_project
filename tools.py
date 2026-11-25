import pandas as pd

def read_csv(csv_path):
    file = pd.read_csv(csv_path)
    return file