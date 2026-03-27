import pandas as pd
import sys

def inspect_excel(file_path):
    try:
        df = pd.read_excel(file_path, nrows=5)
        print(f"\nFile: {file_path}")
        print("Columns:", df.columns.tolist())
        print("First 2 rows:")
        print(df.head(2).to_dict(orient='records'))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    files = [
        "data/Yarn purchase data.xlsx",
        "data/sales final data.xlsx",
        "data/inventory_large.xlsx",
        "data/payments_large.xlsx"
    ]
    for f in files:
        inspect_excel(f"c:/Users/divya/Downloads/textile_ai_project/{f}")
