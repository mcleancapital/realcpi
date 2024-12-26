import schedule
import time
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from datetime import datetime
import os
import subprocess

# File path to your Excel file in the repository
excel_file = './data/sp-500-prices.xlsx'  # Adjust the path if necessary

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

        # Commit and push changes back to the repository
        subprocess.run(["git", "add", excel_file])
        subprocess.run(["git", "commit", "-m", f"Update S&P 500 price for {current_date}"])
        subprocess.run(["git", "push"])

    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the task to run every day at 5 PM Montreal time
schedule.every().day.at("17:00").do(fetch_and_update_price)

print("Scheduler is running. Waiting for the next scheduled task...")
while True:
    schedule.run_pending()
    time.sleep(1)
