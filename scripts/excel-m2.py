import requests
from openpyxl import Workbook, load_workbook
from datetime import datetime
import pandas as pd
import os

# FRED API Setup
API_KEY = "dc0a72da11fb0ffc6f4dc8d31e7afbb5"
FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
SERIES_ID = "M2SL"  # M2 Money Stock (seasonally adjusted)

# Output Excel file
EXCEL_FILE = "./data/m2.xlsx"

# Fetch data from FRED
def get_fred_monthly_data(series_id, api_key):
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "frequency": "m"
    }
    response = requests.get(FRED_BASE, params=params)
    response.raise_for_status()
    data = response.json()
    if "observations" in data:
        return {
            obs["date"]: float(obs["value"])
            for obs in data["observations"]
            if obs["value"] != "."
        }
    else:
        raise Exception(f"No data found for series {series_id}")

# Main logic
try:
    data_dict = get_fred_monthly_data(SERIES_ID, API_KEY)

    # Convert to DataFrame and sort
    df = pd.DataFrame(list(data_dict.items()), columns=["Date", "Value"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Calculate % change vs 12 months ago
    yoy_changes = []
    for i in range(len(df)):
        if i + 12 < len(df):
            current = df.loc[i, "Value"]
            past = df.loc[i + 12, "Value"]
            change = ((current / past) - 1) * 100 if past != 0 else None
            yoy_changes.append(round(change, 2))
        else:
            yoy_changes.append(None)
    df["% Change vs Last Year"] = yoy_changes

    # Save to Excel
    if not os.path.exists(os.path.dirname(EXCEL_FILE)):
        os.makedirs(os.path.dirname(EXCEL_FILE))

    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(["Date", "Value", "% Change vs Last Year"])

    for _, row in df.iterrows():
        ws.append([row["Date"].date(), row["Value"], row["% Change vs Last Year"]])

    wb.save(EXCEL_FILE)
    print(f"✔ M2 data saved to {EXCEL_FILE}")

except Exception as e:
    print(f"❌ Error: {e}")
