import pandas as pd
from datetime import datetime

def update_sp500_html(html_file, excel_file, output_file):
    try:
        print("Step 1: Reading Excel file...")

        # Read Excel file
        df = pd.read_excel(excel_file, sheet_name="Data", usecols=["Date", "Value"], header=0)

        # Drop rows with missing dates or values
        df = df.dropna(subset=["Date", "Value"])
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        # Sort by date ascending
        df = df.sort_values(by="Date").reset_index(drop=True)

        # Calculate % change vs same month last year (12 rows before)
        df["% Change vs Last Year"] = df["Value"].pct_change(periods=12) * 100

        # Calculate numeric dates (days since epoch)
        epoch = datetime(1969, 12, 20)
        df["Date_Numeric"] = (df["Date"] - epoch).dt.days

        # Extract arrays
        date_array = df["Date_Numeric"].tolist()
        value_array = df["Value"].tolist()

        # Format for JavaScript
        formatted_dates = ", ".join(map(str, date_array))
        formatted_values = ", ".join(map(str, value_array))
        formatted_data = f"[[{formatted_dates}], [{formatted_values}], null, null, '', 1, []]"

        # Most recent data
        most_recent_date = df.iloc[-1]["Date"]
        most_recent_value = df.iloc[-1]["Value"]
        most_recent_change = df.iloc[-1]["% Change vs Last Year"]

        formatted_date = most_recent_date.strftime("%b %Y")
        formatted_value = f"{most_recent_value:,.2f}K"

        if pd.isna(most_recent_change):
            formatted_change = ""
        else:
            formatted_change = f" ({most_recent_change:,.2f}% vs last year)"

        # Read HTML content
        print("Step 2: Reading HTML file...")
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Update data array in HTML
        print("Step 3: Updating the data array...")
        data_marker = "<!-- US Nonfarm Payrolls -->"
        if data_marker in html_content:
            data_start = html_content.find(data_marker) + len(data_marker)
            data_end = html_content.find("]]", data_start) + 2
            html_content = (
                html_content[:data_start] +
                "\n" + formatted_data + "\n" +
                html_content[data_end:]
            )
        else:
            print(f"Marker '{data_marker}' not found in HTML.")
            return

        # Update S&P 500 box section
        print("Step 4: Updating the visual box...")
        sp500_marker = '<a class=box href="/nonfarm-payrolls">'
        marker_start = html_content.find(sp500_marker)
        if marker_start == -1:
            print("Box marker not found in HTML.")
            return

        section_end = html_content.find("</a>", marker_start) + 4
        section_content = html_content[marker_start:section_end]

        # Replace value inside <div>
        value_start = section_content.find("<div>", section_content.find("<h3>")) + 5
        value_end = section_content.find("</div>", value_start)
        updated_section = (
            section_content[:value_start] +
            f"{formatted_value}{formatted_change}" +
            section_content[value_end:]
        )

        # Replace date
        date_marker = '<div class="date">'
        date_start = updated_section.find(date_marker) + len(date_marker)
        date_end = updated_section.find("</div>", date_start)
        updated_section = (
            updated_section[:date_start] +
            formatted_date +
            updated_section[date_end:]
        )

        # Replace section in full HTML
        html_content = (
            html_content[:marker_start] +
            updated_section +
            html_content[section_end:]
        )

        # Save updated HTML
        print("Step 5: Writing updated HTML...")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"✅ HTML file '{output_file}' updated successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# File paths
html_file = './economy.html'
excel_file = './data/nonfarm-payrolls.xlsx'
output_file = './economy.html'

# Run the function
update_sp500_html(html_file, excel_file, output_file)
