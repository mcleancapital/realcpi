import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime

# File path to your Excel file in the repository
excel_file = './data/sp-500-prices.xlsx'  # Ensure this path is correct in your repo

def fetch_and_update_price():
    try:
        # URL of the S&P 500 page
        url = "https://www.spglobal.com/spdji/en/indices/equity/sp-500/#overview"
        response = requests.get(url)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the S&P 500 price (update the selector based on the actual HTML structure)
        price_element = soup.select_one('.price-class-selector')  # Update this selector
        if not price_element:
            print("Price element not found on the page.")
            return

        # Extract and format the price
        price = float(price_element.text.replace(',', ''))
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

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function directly (GitHub Actions will call this script)
if __name__ == "__main__":
    fetch_and_update_price()
