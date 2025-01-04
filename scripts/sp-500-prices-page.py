import pandas as pd
import requests
from base64 import b64encode
import re
from openpyxl import load_workbook
from datetime import datetime

# Import win32com.client for fallback
import win32com.client

# Paths for the files
excel_file = './data/sp-500-prices.xlsx'
html_template = './s-p-500-historical-prices/index.html'
output_html = './s-p-500-historical-prices/index.html'

# Read Excel data for general processing
data = pd.read_excel(excel_file, sheet_name="Data", engine="openpyxl")
data["Date"] = pd.to_datetime(data["Date"])
data.sort_values(by="Date", inplace=True)

# Calculate the latest values
latest_date = data.iloc[-1]["Date"]
latest_volume = int(data.iloc[-1]["Value"])

# Fallback function to get C2 value using COM interface
def get_c2_value_via_com(file_path):
    excel = win32com.client.Dispatch("Excel.Application")
    wb = excel.Workbooks.Open(file_path)
    sheet = wb.Sheets("Data")
    wb.RefreshAll()  # Refresh all links and data
    excel.CalculateFull()  # Force recalculation
    c2_value = sheet.Range("C2").Value  # Get value from C2
    wb.Close(SaveChanges=False)
    excel.Quit()
    return c2_value

# Read cell C2 for '% Change vs Last Year' using openpyxl
try:
    wb = load_workbook(excel_file, data_only=True)  # data_only=True retrieves evaluated formula values
    sheet = wb["Data"]
    latest_percentage_change = sheet["C2"].value  # Retrieve the value of cell C2
    print(f"Value of C2 (openpyxl): {latest_percentage_change}")

    # Fallback if value is None
    if latest_percentage_change is None:
        print("openpyxl could not retrieve the value. Falling back to COM interface.")
        latest_percentage_change = get_c2_value_via_com(excel_file)
        print(f"Value of C2 (COM): {latest_percentage_change}")
except Exception as e:
    print(f"Error reading C2 with openpyxl: {e}")
    print("Falling back to COM interface.")
    latest_percentage_change = get_c2_value_via_com(excel_file)
    print(f"Value of C2 (COM): {latest_percentage_change}")

# Handle cases where C2 is None or invalid
if latest_percentage_change is None:
    formatted_percentage_change = "N/A"
else:
    formatted_percentage_change = f"{latest_percentage_change:+.1f}%"

# Format the "let pi" data
dates_since_reference = (data["Date"] - datetime(1969, 11, 20)).dt.days.tolist()
monthly_totals = data["Value"].tolist()
pi_data = f"let pi = [{dates_since_reference}, {monthly_totals}, null, null, '', 1, []];"

# Read the HTML template
with open(html_template, "r", encoding="utf-8") as file:
    html_content = file.read()

# Replace "let pi" data
html_content = re.sub(r"let pi = \[.*?\];", pi_data, html_content, flags=re.DOTALL)

# Replace the values and percentage change
html_content = re.sub(
    r"<b>Current <span class=\"currentTitle\">.*?</span>:</b>.*?\(.*?\)",
    f"<b>Current <span class=\"currentTitle\">Price</span>:</b> {latest_volume:,} ({formatted_percentage_change} vs last year)",
    html_content,
    flags=re.DOTALL
)

# Update the timestamp
html_content = re.sub(
    r"<div id=\"timestamp\">.*?</div>",
    f"<div id=\"timestamp\">{latest_date.strftime('%b %d, %Y')}</div>",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML locally
with open(output_html, "w", encoding="utf-8") as file:
    file.write(html_content)
