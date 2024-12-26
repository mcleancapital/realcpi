import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime
import subprocess

# File path to the Excel file in the repository
excel_file = './data/sp-500-prices.xlsx'

def fetch_and_update_price():
    try:
        # URL of the S&P 500 page
        url = "https://www.spglobal.com/spdji/en/indices/equity/sp-500/#overview"
        
        # Add a User-Agent header to the request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the S&P 500 price (update the selector based on actual HTML structure)
        price_element = soup.select_one('.price-class-selector')  # Replace with the actual selector
        if not price_element:
            print("Price element not found on the page.")
            return

        # Extract and process the price
        price = float(price_element.text.replace(',', '').strip())
        print(f"Fetched S&P 500 Price: {price}")

        # Open the Excel file and append the data
        workbook = load_workbook(excel_file)
        sheet = workbook['Data']

        # Append the new data with the current date and price
        current_date = datetime.now().strftime('%Y-%m-%d')
        sheet.append([current_date, price])

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
