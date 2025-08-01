import os
import pandas as pd
import json

def read_csv_tool(filepath: str) -> str:
    # ... (rest of your function code remains the same)
    try:
        df = pd.read_csv(filepath)
        return df.to_json(orient='records')
    except FileNotFoundError:
        return f"Error: File not found at {filepath}"

def list_directory_tool(path: str) -> str:
    # ... (rest of your function code remains the same)
    try:
        return json.dumps(os.listdir(path))
    except FileNotFoundError:
        return f"Error: Directory not found at {path}"