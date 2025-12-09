#3 different functions for the extraction of 3 different data type files
import pandas as pd

def extract_csv(file_path):
    return pd.read_csv(file_path)

def extract_json(file_path):
    return pd.read_json(file_path)

def extract_excel(file_path):
    return pd.read_excel(file_path)