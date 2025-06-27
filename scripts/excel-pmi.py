import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# File path to the Excel file
EXCEL_FILE_PATH = './data/pmi.xlsx'

# URL and headers
URL = "https://ycharts.com/indicators/us_pmi"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_recent_pmi_data(url):
    """Fetch the most recent PMI data from the YCharts page."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find("div", class_="key-stat-title")
        if not element:
            raise Exception("Failed to find 'key-stat-title' element.")

        text = element.get_text(strip=True)
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            raise Exception("Unexpected format for PMI data.")

        value = float(parts[0])
        date_str = parts[2].replace("for ", "")
        date = datetime.strptime(date_str, "%b %Y").strftime("%Y-%m-%d")

        print(f"Fetched PMI: {value} on {date}")
        return date, value
    except Exception as e:
        print(f"Error fetching PMI data: {e}")
        return None, None

def update_excel(file_path, new_date, new_value):
    try:
        # Load workbook and sheet
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        wb = load_workbook(file_path)
        sheet_name = "Data"
        if sheet_name not in wb.sheetnames:
            print(f"'{sheet_name}' sheet not found.")
            return
        ws = wb[sheet_name]

        # Read existing data
        data = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1]:
                data.append((pd.to_datetime(row[0]).strftime("%Y-%m-%d"), float(row[1])))

        # Check if the latest date is already present
        if data and data[0][0] == new_date:
            print(f"Date {new_date} already in Excel. No update needed.")
            return

        # Prepend the new data
        data.insert(0, (new_date, new_value))
        df = pd.DataFrame(data, columns=["Date", "Value"])

        # Calculate % Change vs Last Year (12 rows down)
        df["% Change vs Last Year"] = (
            (df["Value"] / df["Value"].shift(12) - 1) * 100
        ).round(1)

        # Clear sheet (except header)
        for row in ws["A2:C1000"]:
            for cell in row:
                cell.value = None

        # Write updated data
        for i, row in enumerate(dataframe_to_rows(df, index=False, header=False), start=2):
            for j, value in enumerate(row, start=1):
                ws.cell(row=i, column=j, value=value)

        wb.save(file_path)
        print(f"Excel file updated with PMI for {new_date}.")
    except Exception as e:
        print(f"Error updating Excel: {e}")

if __name__ == "__main__":
    date, value = fetch_recent_pmi_data(URL)
    if date and value:
        update_excel(EXCEL_FILE_PATH, date, value)
