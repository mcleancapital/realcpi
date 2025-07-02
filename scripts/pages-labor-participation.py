import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import re
import os

# Paths for the files
excel_file = './data/labor-participation.xlsx'
html_template = './labor-participation/index.html'
output_html = './labor-participation/index.html'

# Read Excel data
data = pd.read_excel(excel_file, sheet_name="Data", engine="openpyxl")

# Clean and prepare
data["Date"] = pd.to_datetime(data["Date"], format="mixed", errors="coerce")
data.dropna(subset=["Date", "Value"], inplace=True)
data.sort_values(by="Date", inplace=True)

# Extract latest values
latest_date = data.iloc[-1]["Date"]
latest_volume = data.iloc[-1]["Value"]
latest_yoy = data.iloc[-1][2]  # Assuming column C is 3rd column (0-indexed)

# Format the YoY % change text
if pd.isna(latest_yoy):
    yoy_text = ""
else:
    sign = "+" if latest_yoy >= 0 else ""
    yoy_text = f" ({sign}{latest_yoy:.2f}% vs last year)"

# Format the "let pi" data for the chart
dates_since_reference = (data["Date"] - datetime(1969, 12, 20)).dt.days.tolist()
monthly_totals = data["Value"].tolist()
pi_data = f"let pi = [{dates_since_reference}, {monthly_totals}, null, null, '', 0, []];"

# Read the HTML template
with open(html_template, "r", encoding="utf-8") as file:
    html_content = file.read()

# Replace the "let pi" chart data block
html_content = re.sub(
    r"let pi = \[.*?\];",
    pi_data,
    html_content,
    flags=re.DOTALL
)

# Replace the current value and timestamp with YoY text
html_content = re.sub(
    r"<b>Current <span class=\"currentTitle\">.*?</span>:</b>.*?<div id=\"timestamp\">.*?</div>",
    f"<b>Current <span class=\"currentTitle\">Labor Force Participation</span>:</b> {latest_volume:.2f}{yoy_text}"
    f"<div id=\"timestamp\">{latest_date.strftime('%b %Y')}</div>",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML
with open(output_html, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"✔ HTML updated with M2 value {latest_volume:.2f}{yoy_text} for {latest_date.strftime('%b %Y')}")
