import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import load_workbook

# Constants
EXCEL_FILE_PATH = "./data/10-year-treasury-rate.xlsx"
SHEET_NAME = "Data"  # Ensure the sheet is always named "Data"
URL = "https://www.multpl.com/10-year-treasury-rate/table/by-month"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_latest_sp500_pe(url):
    """Fetch the latest S&P 500 P/E ratio from the webpage."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data, Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        table_rows = soup.find_all("tr")

        if len(table_rows) < 2:
            raise Exception("No valid data found in the table.")

        latest_data = table_rows[1].find_all("td")  # Second row contains latest data
        if len(latest_data) < 2:
            raise Exception("Unexpected data format.")

        # Extract and clean the date
        latest_date = latest_data[0].text.strip()
        latest_value_str = latest_data[1].text.strip().replace("†", "").replace("\n", "").strip()

        # Convert the value to a float
        latest_value = float(latest_value_str.replace("%", ""))

        # Convert date to YYYY-MM-DD format
        latest_date = datetime.strptime(latest_date, "%b %d, %Y").strftime("%Y-%m-%d")

        print(f"Fetched Latest Data - Date: {latest_date}, Value: {latest_value}")
        return latest_date, latest_value
    except Exception as e:
        print(f"Error fetching S&P 500 P/E data: {e}")
        return None, None

def update_excel(file_path, latest_date, latest_value):
    """Update Excel file with new data while ensuring sheet name is correct."""
    try:
        # Load existing workbook or create a new one
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=SHEET_NAME, dtype={"Date": str})
        else:
            df = pd.DataFrame(columns=["Date", "Value"])

        # Convert 'Date' column to string format YYYY-MM-DD
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime("%Y-%m-%d")

        # Ensure `latest_date` is also in YYYY-MM-DD format
        latest_date_str = datetime.strptime(latest_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        # Check if the latest date is the 1st of the month
        is_first_of_month = datetime.strptime(latest_date, "%Y-%m-%d").day == 1

        # If the latest date already exists, update the first row
        if not df.empty and df.iloc[0]["Date"] == latest_date_str:
            print("Latest date already exists. Updating value instead of inserting new row.")
            df.at[0, "Value"] = latest_value
        elif is_first_of_month:
            # Insert new row at the top only if it's the first of the month
            new_row = pd.DataFrame([[latest_date_str, latest_value]], 
                                   columns=["Date", "Value"])
            df = pd.concat([new_row, df], ignore_index=True)
            print(f"Added new data: {latest_date}, Value: {latest_value}")
        else:
            # Update the most recent row if new data is not the 1st of the month
            print("Latest data is not from the 1st of the month. Updating most recent row instead.")
            df.at[0, "Date"] = latest_date_str
            df.at[0, "Value"] = latest_value

        # Save the updated DataFrame to Excel
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False)

        print(f"Excel file updated successfully in sheet '{SHEET_NAME}': {file_path}")

    except Exception as e:
        print(f"Error updating Excel file: {e}")

if __name__ == "__main__":
    # Fetch latest S&P 500 P/E data
    latest_date, latest_value = fetch_latest_sp500_pe(URL)

    # Update the Excel file if data was successfully fetched
    if latest_date and latest_value:
        update_excel(EXCEL_FILE_PATH, latest_date, latest_value)
