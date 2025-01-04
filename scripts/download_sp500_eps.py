import os
import requests
from datetime import datetime

EXCEL_URL = "https://www.spglobal.com/spdji/en/documents/additional-material/sp-500-eps-est.xlsx"
SAVE_DIR = "./data"  # Relative to the /scripts directory

def download_excel():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"sp500_eps_{today}.xlsx"
    filepath = os.path.join(SAVE_DIR, filename)

    try:
        if not os.path.exists(SAVE_DIR):
            raise FileNotFoundError(f"Directory not found: {SAVE_DIR}")

        response = requests.get(EXCEL_URL)
        response.raise_for_status()

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"File saved successfully at: {filepath}")
    except Exception as e:
        print(f"Error: {e}")

if datetime.now().day == 4:
    download_excel()
