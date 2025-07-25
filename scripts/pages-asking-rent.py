import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import re

# File paths
excel_file = './data/asking-rent.xlsx'
html_template = './asking-rent/index.html'
output_html = './asking-rent/index.html'

# Load Excel
data = pd.read_excel(excel_file, sheet_name="Data", engine="openpyxl")
data["Date"] = pd.to_datetime(data["Date"])
data.sort_values(by="Date", inplace=True)

# Extract latest values
latest_row = data.iloc[-1]
latest_date = latest_row["Date"]
latest_value = int(latest_row["Value"])

# Read % change from C2
try:
    wb = load_workbook(excel_file, data_only=True)
    sheet = wb["Data"]
    latest_percentage_change = sheet["C2"].value
except Exception as e:
    print(f"Error reading C2: {e}")
    latest_percentage_change = None

formatted_percentage_change = f"{latest_percentage_change:+.1f}%" if latest_percentage_change is not None else "N/A"

# Chart data
dates_since_ref = (data["Date"] - datetime(1969, 12, 20)).dt.days.tolist()
values = data["Value"].tolist()
date_str = ",".join(map(str, dates_since_ref))
value_str = ",".join(map(str, values))
pi_js = f"let pi = [[{date_str}],[{value_str}],null,null,'',1,[]];"

# Load HTML
with open(html_template, "r", encoding="utf-8") as file:
    html_content = file.read()

# Replace chart data
html_content = re.sub(
    r"let pi = \[.*?\];",
    pi_js,
    html_content,
    flags=re.DOTALL
)

# Replace text content
def replace_current_text(match):
    return f'{match.group(1)}${latest_value:,.0f} ({formatted_percentage_change} vs last year)'

html_content = re.sub(
    r'(<b>Current <span class="currentTitle">US Median Asking Rent</span>:</b>\s*)\$?[\d,]+(?:\s*\(.*?\))?',
    replace_current_text,
    html_content
)

# Replace timestamp
html_content = re.sub(
    r'(<div id="timestamp">).*?(</div>)',
    rf"\1{latest_date.strftime('%b %Y')}\2",
    html_content
)

# Save result
with open(output_html, "w", encoding="utf-8") as file:
    file.write(html_content)

print("✅ HTML updated with latest rent + chart data.")
