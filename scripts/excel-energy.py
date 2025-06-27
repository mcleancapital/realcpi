import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import xlwings as xw

# === CONFIG ===
EXCEL_FILE_PATH = './data/energy.xlsx'
SHEET_NAME = "Data"
URL = "https://ycharts.com/indicators/us_primary_energy_consumption"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_recent_energy_data(url):
    """Fetch the most recent energy consumption data from YCharts."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find("div", class_="key-stat-title")
        if not element:
            raise Exception("Could not find 'key-stat-title' on the page.")

        text = element.get_text(strip=True)
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            raise Exception("Unexpected data format from YCharts.")

        value = float(parts[0].replace('Q', ''))
        date = datetime.strptime(parts[2].replace("for ", ""), "%b %Y").strftime("%Y-%m-%d")

        print(f"✔️  Fetched energy value: {value}Q BTU for {date}")
        return date, value
    except Exception as e:
        print(f"❌ Error fetching energy data: {e}")
        return None, None


def update_excel_with_energy(file_path, recent_date, recent_value):
    """Update Excel with new energy data and replace formulas with static values."""
    try:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return

        # Load workbook with openpyxl
        wb = load_workbook(file_path)
        if SHEET_NAME not in wb.sheetnames:
            print(f"❌ Sheet '{SHEET_NAME}' not found.")
            return
        ws = wb[SHEET_NAME]

        most_recent = ws.cell(row=2, column=1).value
        if most_recent and pd.to_datetime(most_recent).strftime("%Y-%m-%d") == recent_date:
            print(f"ℹ️  {recent_date} already exists — skipping insert.")
            return

        # Insert new row at top
        ws.insert_rows(2)
        ws.cell(row=2, column=1, value=recent_date)
        ws.cell(row=2, column=2, value=recent_value)

        # Add formulas in column C
        for row in range(2, ws.max_row + 1):
            ws.cell(row=row, column=3, value=f"=(B{row}/B{row+12}-1)*100")

        # Save so xlwings can open with formulas in place
        wb.save(file_path)
        print("💾 Excel saved with formulas. Launching Excel for calculation...")

        # Open with xlwings for calculation and value replacement
        app = xw.App(visible=False)
        wb_xlw = app.books.open(file_path)
        sheet = wb_xlw.sheets[SHEET_NAME]

        # Force full calculation
        app.calculate()
        app.api.CalculateFullRebuild()

        # Replace formulas in column C with their evaluated values
        last_row = sheet.range("B1").end("down").row
        for row in range(2, last_row + 1):
            cell = sheet.range(f"C{row}")
            val = cell.value
            cell.value = val  # overwrite with static number

        wb_xlw.save()
        wb_xlw.close()
        app.quit()
        print("✅ Excel updated: formulas evaluated and saved as values.")

    except Exception as e:
        print(f"❌ Error updating Excel: {e}")


if __name__ == "__main__":
    date, value = fetch_recent_energy_data(URL)
    if date and value:
        update_excel_with_energy(EXCEL_FILE_PATH, date, value)
