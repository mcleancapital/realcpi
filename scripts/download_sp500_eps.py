import os
import requests
from datetime import datetime

# URL of the Excel file
EXCEL_URL = "https://www.spglobal.com/spdji/en/documents/additional-material/sp-500-eps-est.xlsx"
SAVE_DIR = "data"  # Directory to save the Excel files

def download_excel():
    """
    Download the Excel file and save it locally with a timestamped filename.
    """
    # Ensure the directory exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Generate filename with the current date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"sp500_eps_{today}.xlsx"
    filepath = os.path.join(SAVE_DIR, filename)

    try:
        # Download the file
        response = requests.get(EXCEL_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Save the file
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"Downloaded successfully: {filepath}")
    except Exception as e:
        print(f"Failed to download the file: {e}")

# Schedule the script to run only on the 4th day of the month
if datetime.now().day == 4:
    download_excel()
