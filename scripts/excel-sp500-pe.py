import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Constants
EXCEL_FILE_PATH = "./data/sp-500-pe.xlsx"
URL = "https://www.multpl.com/s-p-500-pe-ratio/table/by-month"
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

        latest_date = latest_data[0].text.strip()
        latest_value = float(latest_data[1].text.strip().replace("†", "").replace("\n", ""))

        # Convert date to YYYY-MM-DD format
        latest_date = datetime.strptime(latest_date, "%b %d, %Y").strftime("%Y-%m-%d")

        print(f"Fetched Latest Data - Date: {latest_date}, Value: {latest_value}")
        return latest_date, latest_value
    except Exception as e:
        print(f"Error fetching S&P 500 P/E data: {e}")
        return None, None

def update_excel(file_path, latest_date, latest_value):
    """Update Excel file with new data while handling monthly updates."""
    try:
        # Load existing data or create a new DataFrame
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            df = pd.DataFrame(columns=["Date", "Value", "% Change vs Last Year"])

        # Convert 'Date' column to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

        # Check if latest_date already exists in the file
        if not df.empty and df.iloc[0]["Date"].strftime("%Y-%m-%d") == latest_date:
            print("Latest date already exists. Updating value instead of inserting new row.")
            df.at[0, "Value"] = latest_value
        else:
            # Calculate % Change vs Last Year
            last_year_date = (datetime.strptime(latest_date, "%Y-%m-%d").replace(year=datetime.strptime(latest_date, "%Y-%m-%d").year - 1)).strftime("%Y-%m-%d")
            last_year_value = df[df["Date"] == last_year_date]["Value"].values
            percent_change = ((latest_value - last_year_value[0]) / last_year_value[0]) * 100 if len(last_year_value) > 0 else None

            # Insert new row at the top
            new_row = pd.DataFrame([[latest_date, latest_value, percent_change]], columns=["Date", "Value", "% Change vs Last Year"])
            df = pd.concat([new_row, df], ignore_index=True)

            print(f"Added new data: {latest_date}, Value: {latest_value}, % Change vs Last Year: {percent_change}")

        # Save to Excel
        df.to_excel(file_path, index=False)
        print(f"Excel file updated successfully: {file_path}")
    except Exception as e:
        print(f"Error updating Excel file: {e}")

if __name__ == "__main__":
    # Fetch latest S&P 500 P/E data
    latest_date, latest_value = fetch_latest_sp500_pe(URL)

    # Update the Excel file if data was successfully fetched
    if latest_date and latest_value:
        update_excel(EXCEL_FILE_PATH, latest_date, latest_value)
