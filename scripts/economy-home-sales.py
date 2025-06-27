import pandas as pd
from datetime import datetime

def update_sp500_html(html_file, excel_file, output_file):
    try:
        print("Step 1: Reading Excel file...")
        # Read the Excel file
        df = pd.read_excel(excel_file, sheet_name="Data", usecols=["Date", "Value"], header=0)

        # Drop rows where 'Date' or 'Value' is missing
        df = df.dropna(subset=["Date", "Value"])

        # Convert 'Date' to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])  # Remove rows with invalid dates

        # Calculate % change vs same month one year ago
        df = df.sort_values("Date", ascending=True).reset_index(drop=True)
        df["% Change vs Last Year"] = df["Value"].pct_change(periods=12) * 100

        # Drop rows without change info
        df = df.dropna(subset=["% Change vs Last Year"])

        # Calculate numeric representation of dates relative to 1969-12-20
        epoch = datetime(1969, 12, 20)
        df["Date_Numeric"] = (df["Date"] - epoch).dt.days

        # Extract arrays for the output
        date_array = df["Date_Numeric"].tolist()
        value_array = df["Value"].tolist()

        # Format arrays as strings
        formatted_dates = ", ".join(map(str, date_array))
        formatted_values = ", ".join(map(str, value_array))

        # Combine the formatted array with the required suffix
        formatted_data = f"[[{formatted_dates}], [{formatted_values}], null, null, '', 1, []]"

        # Get the most recent values
        most_recent_date = df.iloc[-1]["Date"]
        most_recent_value = int(df.iloc[-1]["Value"])
        most_recent_change = df.iloc[-1]["% Change vs Last Year"]

        # Format the date, value, and change
        formatted_date = most_recent_date.strftime("%b %Y")
        formatted_value = f"{most_recent_value:,}M"
        formatted_change = f"({most_recent_change:+.1f}% vs last year)"

        print("Step 2: Reading HTML file...")
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Step 3: Update the data section in HTML
        print("Step 3: Updating the data section in HTML...")
        data_marker = "<!-- Existing Home Sales -->"
        if data_marker in html_content:
            data_start = html_content.find(data_marker) + len(data_marker)
            data_end = html_content.find("]]", data_start) + 2
            html_content = (
                html_content[:data_start] +
                "\n" + formatted_data + "\n" +
                html_content[data_end:]
            )
        else:
            print(f"Data section marker '{data_marker}' not found.")
            return

        # Step 4: Update the <a class=box> section
        print("Step 4: Updating value and date in HTML box...")
        box_marker = '<a class=box href="/home-sales">'
        marker_start = html_content.find(box_marker)
        if marker_start == -1:
            print("Box section not found.")
            return
        section_end = html_content.find("</a>", marker_start) + 4
        section = html_content[marker_start:section_end]

        # Update value
        value_start = section.find("<div>", section.find("<h3>")) + 5
        value_end = section.find("</div>", value_start)
        updated_value = f"{formatted_value} {formatted_change}"
        section = section[:value_start] + updated_value + section[value_end:]

        # Update date
        date_marker = '<div class="date">'
        date_start = section.find(date_marker) + len(date_marker)
        date_end = section.find("</div>", date_start)
        section = section[:date_start] + formatted_date + section[date_end:]

        # Replace section
        html_content = html_content[:marker_start] + section + html_content[section_end:]

        # Step 5: Write updated HTML
        print("Step 5: Writing updated HTML...")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"✅ HTML file '{output_file}' updated successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# File paths
html_file = './economy.html'
excel_file = './data/existing-home-sales.xlsx'
output_file = './economy.html'

# Run the update function
update_sp500_html(html_file, excel_file, output_file)
