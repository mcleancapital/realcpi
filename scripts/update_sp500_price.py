import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime
import subprocess

# File path to your Excel file in the repository
excel_file = './data/sp-500-prices.xlsx'

def fetch_and_update_price():
    try:
        # Yahoo Finance URL for S&P 500 (^GSPC) historical data
        url = "https://ca.finance.yahoo.com/quote/%5EGSPC/history"
        response = requests.get(url)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the historical price table
        table = soup.find('table', {'data-test': 'historical-prices'})
        if not table:
            print("Historical prices table not found.")
            return

        # Get the first row of the table (latest data)
        rows = table.find_all('tr')
        if len(rows) < 2:
            print("No data rows found in the table.")
            return

        # Extract date and closing price from the latest row
        latest_row = rows[1].find_all('td')
        if len(latest_row) < 6:
            print("Unexpected row format in the table.")
            return

        # Parse date and price
        date_str = latest_row[0].text.strip()
        closing_price = float(latest_row[4].text.replace(',', '').strip())
        current_date = datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')
        print(f"Fetched S&P 500 Closing Price: {closing_price} on {current_date}")

        # Open the Excel file and append the data
        workbook = load_workbook(excel_file)
        sheet = workbook['Data']

        # Append the new data with the current date and price
        sheet.append([current_date, closing_price])

        # Save the updated Excel file
        workbook.save(excel_file)
        print("Excel file updated successfully.")

        # Commit and push changes back to the repository
        subprocess.run(["git", "add", excel_file])
        subprocess.run(["git", "commit", "-m", f"Update S&P 500 price for {current_date}"])
        subprocess.run(["git", "push"])

        print("Changes committed and pushed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_update_price()
