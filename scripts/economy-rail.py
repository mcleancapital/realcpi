import pandas as pd
from datetime import datetime
import re

def update_m2_html(html_file, excel_file, output_file):
    try:
        print("Step 1: Reading Excel file...")
        df = pd.read_excel(excel_file, sheet_name="Data", header=0)

        # Drop rows with missing data
        df = df.dropna(subset=["Date", "Value"])
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.sort_values(by="Date").reset_index(drop=True)

        # Prepare data arrays
        epoch = datetime(1969, 12, 20)
        df["Date_Numeric"] = (df["Date"] - epoch).dt.days
        date_array = df["Date_Numeric"].tolist()
        value_array = df["Value"].tolist()
        formatted_data = f"[[{', '.join(map(str, date_array))}], [{', '.join(map(str, value_array))}], null, null, '', 0, []]"

        # Get latest data point
        latest_date = df.iloc[-1]["Date"]
        latest_value = df.iloc[-1]["Value"]
        try:
            latest_yoy = df.iloc[-1][2]  # Assumes column C is the YoY % change
            if pd.isna(latest_yoy):
                yoy_text = ""
            else:
                sign = "+" if latest_yoy >= 0 else ""
                yoy_text = f" ({sign}{latest_yoy:.2f}% vs last year)"
        except Exception:
            yoy_text = ""

        formatted_value = f"{latest_value:,.2f}{yoy_text}"
        formatted_date = latest_date.strftime("%b %Y")

        print("Step 2: Reading HTML file...")
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        print("Step 3: Updating chart data...")
        data_marker = "<!-- Rail -->"
        if data_marker in html_content:
            data_start = html_content.find(data_marker) + len(data_marker)
            data_end = html_content.find("]]", data_start) + 2
            html_content = (
                html_content[:data_start] +
                "\n" + formatted_data + "\n" +
                html_content[data_end:]
            )
        else:
            print(f"Data marker '{data_marker}' not found.")
            return

        print("Step 4: Updating summary box...")
        box_marker = '<a class=box href="/rail">'
        box_start = html_content.find(box_marker)
        if box_start == -1:
            print("Summary box for M2 not found.")
            return

        box_end = html_content.find("</a>", box_start) + 4
        box_content = html_content[box_start:box_end]

        # Replace value
        value_start = box_content.find("<div>", box_content.find("<h3>")) + 5
        value_end = box_content.find("</div>", value_start)
        box_content = (
            box_content[:value_start] +
            formatted_value +
            box_content[value_end:]
        )

        # Replace date
        date_marker = '<div class="date">'
        date_start = box_content.find(date_marker) + len(date_marker)
        date_end = box_content.find("</div>", date_start)
        box_content = (
            box_content[:date_start] +
            formatted_date +
            box_content[date_end:]
        )

        # Update HTML
        html_content = html_content[:box_start] + box_content + html_content[box_end:]

        print("Step 5: Saving updated HTML...")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"✔ HTML file '{output_file}' updated successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# File paths
html_file = './economy.html'
excel_file = './data/rail.xlsx'
output_file = './economy.html'

# Run the update
update_m2_html(html_file, excel_file, output_file)
