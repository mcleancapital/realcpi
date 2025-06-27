import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

# File path to the Excel file
EXCEL_FILE_PATH = './data/existing-home-sales.xlsx'

# URL and headers
URL = "https://ycharts.com/indicators/us_existing_home_sales"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_recent_cpi_data(url):
    """Fetch the most recent Existing Home Sales data from YCharts."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        cpi_element = soup.find("div", class_="key-stat-title")
        if not cpi_element:
            raise Exception("Element with class 'key-stat-title' not found.")

        cpi_text = cpi_element.get_text(strip=True)
        parts = cpi_text.split(maxsplit=2)
        if len(parts) < 3:
            raise Exception("Unexpected CPI format.")

        recent_value = float(parts[0].replace("M", ""))
        recent_date_str = parts[2].replace("for ", "")
        recent_date = datetime.strptime(recent_date_str, "%b %Y").strftime("%Y-%m-%d")

        print(f"Fetched: {recent_value}M for {recent_date}")
        return recent_date, recent_value
    except Exception as e:
        print(f"Error fetching CPI data: {e}")
        return None, None

def update_excel(file_path, recent_date, recent_value):
    """Update the Excel file with static % change calculation in column C."""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        df = pd.read_excel(file_path, sheet_name="Data")

        # Ensure correct columns and drop rows with missing values
        df = df[["Date", "Value"]].dropna()
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date", ascending=False).reset_index(drop=True)

        # Insert the new data if not duplicate
        if not (df["Date"].dt.strftime("%Y-%m-%d") == recent_date).any():
            new_row = pd.DataFrame({"Date": [recent_date], "Value": [recent_value]})
            df = pd.concat([new_row, df], ignore_index=True)

        # Sort again and reset index
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date", ascending=False).reset_index(drop=True)

        # Calculate % Change vs Last Year
        df["% Change vs Last Year"] = df["Value"].pct_change(periods=12) * 100

        # Write back to Excel
        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="Data", index=False)

        print(f"✅ Excel updated: {file_path}")
    except Exception as e:
        print(f"❌ Error updating Excel file: {e}")

if __name__ == "__main__":
    recent_date, recent_value = fetch_recent_cpi_data(URL)
    if recent_date and recent_value:
        update_excel(EXCEL_FILE_PATH, recent_date, recent_value)
