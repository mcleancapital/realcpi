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
    """Fetch the most recent energy data from YCharts."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        elem = soup.find("div", class_="key-stat-title")
        if not elem:
            raise Exception("Missing key-stat-title on page.")

        text = elem.get_text(strip=True)
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            raise Exception("Unexpected format.")

        value = float(parts[0].replace('Q', ''))
        date = datetime.strptime(parts[2].replace("for ", ""), "%b %Y").strftime("%Y-%m-%d")
        print(f"✔️  Fetched energy data: {value}Q BTU for {date}")
        return date, value
    except Exception as e:
        print(f"❌ Error fetching energy data: {e}")
        return None, None


def update_excel_with_energy(file_path, recent_date, recent_value):
    """Insert the new data and update formulas in Excel, then convert to values with xlwings."""
    try:
        if not os.path.exists(file_path):
            print(f"❌ Excel file not found: {file_path}")
            return

        wb = load_workbook(file_path)
        if SHEET_NAME not in wb.sheetnames:
            print(f"❌ Sheet '{SHEET_NAME}' not found.")
            return
        ws = wb[SHEET_NAME]

        most_recent = ws.cell(row=2, column=1).value
        if most_recent and pd.to_datetime(most_recent).strftime("%Y-%m-%d") == recent_date:
            print(f"ℹ️  {recent_date} already exists — skipping insert.")
            return

        ws.insert_rows(2)
        ws.cell(row=2, column=1, value=recent_date)
        ws.cell(row=2, column=2, value=recent_value)

        for row in range(2, ws.max_row + 1):
            ws.cell(row=row, column=3, value=f"=(B{row}/B{row+12}-1)*100")

        wb.save(file_path)
        print("💾 Excel updated with formulas. Launching Excel for evaluation...")

        app = xw.App(visible=False)
        wb_xlw = app.books.open(file_path)
        sheet = wb_xlw.sheets[SHEET_NAME]

        for row in range(2, sheet.range("A1").end("down").row + 1):
            val = sheet.range(f"C{row}").value
            sheet.range(f"C{row}").value = val  # Overwrite formula with evaluated value

        wb_xlw.save()
        wb_xlw.close()
        app.quit()
        print("✅ Formulas evaluated and saved as values.")
    except Exception as e:
        print(f"❌ Error updating Excel: {e}")


if __name__ == "__main__":
    date, value = fetch_recent_energy_data(URL)
    if date and value:
        update_excel_with_energy(EXCEL_FILE_PATH, date, value)
