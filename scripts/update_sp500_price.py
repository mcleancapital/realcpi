import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime
import subprocess

# File path to the Excel file in the repository
excel_file = './data/sp-500-prices.xlsx'  # Adjust if necessary

def fetch_and_update_price():
    try:
        # URL of the S&P 500 page
        url = "https://www.spglobal.com/spdji/en/indices/equity/sp-500/#overview"
        response = requests.get(url)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the S&P 500 price (update the selector based on actual HTML structure)
        price_element = soup.select_one('.price-class-selector')  # Replace with actual CSS selector
        if not price_element:
            print("Price element not found on the page.")
            return

        # Extract and process the price
        price = float(price_element.text.replace(',', '').strip())
        print(f"Fetched S&P 500 Price: {price}")

        # Open the Excel file and load the "Data" sheet
        workbook = load_workbook(excel_file)
        sheet = workbook['Data']

        # Debug: Print the existing rows in the Excel sheet
        print("Current Excel content:")
        for row in sheet.iter_rows(values_only=True):
            print(row)

        # Append the new data with the current date and price
        current_date = datetime.now().strftime('%Y-%m-%d')
        sheet.append([current_date, price])

        # Save the updated Excel file
        workbook.save(excel_file)
        print("Excel file updated successfully.")

        # Debug: Print the updated rows in the Excel sheet
        print("Updated Excel content:")
        for row in sheet.iter_rows(values_only=True):
            print(row)

        # Commit and push changes back to the repository
        subprocess.run(["git", "add", excel_file])
        subprocess.run(["git", "commit", "-m", f"Update S&P 500 price for {current_date}"])
        subprocess.run(["git", "push"])

        print("Changes committed and pushed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the function when the script is run
if __name__ == "__main__":
    fetch_and_update_price()
