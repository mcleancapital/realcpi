import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import re

# Paths for the files
excel_file = './data/population.xlsx'
html_template = './population/index.html'
output_html = './population/index.html'

# Read Excel data
data = pd.read_excel(excel_file, sheet_name="Data", engine="openpyxl")
data["Date"] = pd.to_datetime(data["Date"])
data.sort_values(by="Date", inplace=True)

# Calculate the latest values
latest_date = data.iloc[-1]["Date"]
latest_volume = int(data.iloc[-1]["Value"])

# Calculate "B2 / B14 - 1" using the most recent date and the closest match 12 months prior
try:
    # Ensure DataFrame is sorted in descending order (most recent first)
    data = data.sort_values(by="Date", ascending=False).reset_index(drop=True)

    # B2 is simply the most recent entry
    b2_row = data.iloc[0]  # Most recent row
    b2_date = b2_row["Date"]
    b2 = b2_row["Value"]

    # Find the closest match from approximately 12 months before
    one_year_ago = b2_date - pd.DateOffset(years=1)
    
    # Select the closest available row from at most one year ago
    b14_candidates = data[data["Date"] <= one_year_ago]
    if not b14_candidates.empty:
        b14_row = b14_candidates.iloc[-1]  # Pick the closest available row
        b14 = b14_row["Value"]
        # Calculate percentage change
        percentage_change = (b2 / b14 - 1) * 100
        formatted_percentage = f" (+{percentage_change:.1f}% vs last year)" if percentage_change >= 0 else f" ({percentage_change:.1f}% vs last year)"
    else:
        formatted_percentage = " (N/A vs last year)"

    latest_percentage_change = formatted_percentage

except Exception as e:
    print(f"Error calculating percentage change: {e}")
    formatted_percentage = " (N/A vs last year)"
    latest_percentage_change = formatted_percentage

# Format the "let pi" data for JavaScript (ensuring it properly formats for the chart)
dates_since_reference = "[" + ",".join(map(str, (data["Date"] - datetime(1969, 12, 20)).dt.days.tolist())) + "]"
monthly_totals = "[" + ",".join(map(str, data["Value"].tolist())) + "]"
pi_data = f"let pi = [{dates_since_reference}, {monthly_totals}, null, null, '', 1, []];"

# Read the HTML template
with open(html_template, "r", encoding="utf-8") as file:
    html_content = file.read()

# Replace "let pi" data inside the HTML file
html_content = re.sub(r"let pi = \[.*?\];", pi_data, html_content, flags=re.DOTALL)

# Replace the values and percentage change
html_content = re.sub(
    r"<b>Current <span class=\"currentTitle\">.*?</span>:</b>.*?\(.*?\)",
    f"<b>Current <span class=\"currentTitle\">US Population</span>:</b> {latest_volume:,}M {formatted_percentage}",
    html_content,
    flags=re.DOTALL
)

# Update the timestamp
html_content = re.sub(
    r"<div id=\"timestamp\">.*?</div>",
    f"<div id=\"timestamp\">{latest_date.strftime('%b %Y')}</div>",
    html_content,
    flags=re.DOTALL
)

# Save the updated HTML locally
with open(output_html, "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file updated successfully!")
