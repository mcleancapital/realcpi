import os
import pandas as pd
from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# File path to the Excel file
EXCEL_FILE_PATH = './data/cpi.xlsx'

# URL and headers for web scraping
URL = "https://ycharts.com/indicators/us_consumer_price_index_yoy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_recent_cpi_data(url):
    """Fetch the most recent CPI data from the YCharts page."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        cpi_element = soup.find("div", class_="key-stat-title")
        if not cpi_element:
            raise Exception("Failed to find the element with class 'key-stat-title'.")

        cpi_text = cpi_element.get_text(strip=True)
        parts = cpi_text.split(maxsplit=2)
        if len(parts) < 2:
            raise Exception("Unexpected format for CPI data.")

        recent_value = float(parts[0].replace('%', ''))  # Extract CPI value
        recent_date_str = parts[2].replace("for ", "")  # Clean up the date
        recent_date = datetime.strptime(recent_date_str, "%b %Y").strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD format

        print(f"Fetched CPI data - Value: {recent_value}, Date: {recent_date}")
        return recent_date, recent_value
    except Exception as e:
        print(f"Error fetching CPI data: {e}")
        return None, None

def update_excel(file_path, recent_date, recent_value):
    """Update the Excel file with the most recent CPI data and recalculate formulas."""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        wb = load_workbook(file_path)
        sheet_name = "Data"
        if sheet_name not in wb.sheetnames:
            print(f"'{sheet_name}' sheet not found in the workbook.")
            return
        ws = wb[sheet_name]

        # Check the most recent date in A2
        most_recent_date_in_excel = ws.cell(row=2, column=1).value
        if most_recent_date_in_excel:
            most_recent_date_in_excel = pd.to_datetime(most_recent_date_in_excel).strftime("%Y-%m-%d")

        if most_recent_date_in_excel == recent_date:
            print(f"Recent date {recent_date} already exists in the Excel file. No update needed.")
            return

        # Insert new data
        ws.insert_rows(2)
        ws.cell(row=2, column=1, value=recent_date)  # Date
        ws.cell(row=2, column=2, value=recent_value)  # CPI Value

        # Update formulas in column C
        for row in range(2, ws.max_row + 1):
            ws.cell(row=row, column=3, value=f"=(B{row}/B{row+12}-1)*100")

        print(f"Added new data - Date: {recent_date}, Value: {recent_value}, Updated formulas in column C.")

        # Save and close workbook
        wb.save(file_path)
        print(f"Excel file updated successfully: {file_path}")

        # Recalculate formulas and extract results
        extract_formulas_and_values(file_path)

    except Exception as e:
        print(f"Error updating Excel file: {e}")

def extract_formulas_and_values(file_path):
    """Extract and display formulas and recalculated values from column C."""
    try:
        # Load workbook with formulas
        wb = load_workbook(file_path, data_only=False)
        ws = wb["Data"]

        # Extract formulas from column C
        column_c_formulas = [ws.cell(row=row, column=3).value for row in range(1, ws.max_row + 1)]

        # Save and reload workbook to force recalculation
        wb.save(file_path)
        wb = load_workbook(file_path, data_only=True)  # Load calculated values
        ws = wb["Data"]

        # Extract recalculated values from column C
        column_c_values = [ws.cell(row=row, column=3).value for row in range(1, ws.max_row + 1)]

        # Display results
        print("\n--- Column C: Formulas ---")
        for i, formula in enumerate(column_c_formulas[:10], 1):
            print(f"Row {i}: {formula}")

        print("\n--- Column C: Values ---")
        for i, value in enumerate(column_c_values[:10], 1):
            print(f"Row {i}: {value}")

    except Exception as e:
        print(f"Error extracting formulas and values: {e}")

if __name__ == "__main__":
    # Fetch latest CPI data
    recent_date, recent_value = fetch_recent_cpi_data(URL)

    # Update Excel file if new data is found
    if recent_date and recent_value:
        update_excel(EXCEL_FILE_PATH, recent_date, recent_value)
