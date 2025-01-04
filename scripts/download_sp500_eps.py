import os
import requests
from datetime import datetime

# URL of the Excel file
EXCEL_URL = "https://www.spglobal.com/spdji/en/documents/additional-material/sp-500-eps-est.xlsx"
SAVE_DIR = "../data"  # Path to the data directory relative to the script's location

def download_excel():
    """
    Download the Excel file and save it in the /data/ directory with a timestamped filename.
    """
    # Generate filename with the current date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"sp500_eps_{today}.xlsx"
    filepath = os.path.join(SAVE_DIR, filename)

    try:
        # Ensure the save directory exists
        if not os.path.exists(SAVE_DIR):
            raise FileNotFoundError(f"Directory not found: {SAVE_DIR}")

        # Download the file
        response = requests.get(EXCEL_URL)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the file
        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"File saved successfully: {filepath}")
    except Exception as e:
        print(f"Error: {e}")

if datetime.now().day == 4:
    download_excel()
else:
    print("Not the 4th day of the month.")
