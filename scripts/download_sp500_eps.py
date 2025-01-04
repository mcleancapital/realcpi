import os
import requests
from datetime import datetime

# URL of the Excel file
EXCEL_URL = "https://www.spglobal.com/spdji/en/documents/additional-material/sp-500-eps-est.xlsx"
SAVE_DIR = "./data"  # Path to the data directory

def download_excel():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"sp500_eps_{today}.xlsx"
    filepath = os.path.join(SAVE_DIR, filename)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.spglobal.com/",
    }

    try:
        if not os.path.exists(SAVE_DIR):
            raise FileNotFoundError(f"Directory not found: {SAVE_DIR}")

        response = requests.get(EXCEL_URL, headers=headers)
        response.raise_for_status()

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"File saved successfully at: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if datetime.now().day == 4:
    download_excel()
