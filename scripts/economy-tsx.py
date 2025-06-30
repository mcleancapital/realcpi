import pandas as pd
from datetime import datetime

def update_sp500_html(html_file, excel_file, output_file):
    try:
        print("Step 1: Reading Excel file...")
        # Read the Excel file
        df = pd.read_excel(excel_file, sheet_name="Data", usecols=["Date", "Value"], header=0)

        # Calculate "B2 / B14 - 1" using the most recent date and the closest match 12 months prior
        try:
            # Ensure DataFrame is sorted in descending order (most recent first)
            df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)

            # B2 is simply the most recent entry
            b2_row = df.iloc[0]  # Most recent row
            b2_date = b2_row["Date"]
            b2 = b2_row["Value"]

            # Find the closest match from approximately 12 months before
            one_year_ago = b2_date - pd.DateOffset(years=1)
            b14_row = df[df["Date"] <= one_year_ago].iloc[0]  # First available row within the last 12 months
            b14 = b14_row["Value"]

            # Calculate percentage change
            percentage_change = (b2 / b14 - 1) * 100
            formatted_percentage = f" ({percentage_change:.1f}% vs last year)" if percentage_change >= 0 else f" ({percentage_change:.1f}% vs last year)"
        except Exception as e:
            print(f"Error calculating percentage change: {e}")
            formatted_percentage = " (N/A vs last year)"
        
        # Drop rows where 'Date' or 'Value' is missing
        df = df.dropna(subset=["Date", "Value"])

        # Convert 'Date' to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])  # Remove rows with invalid dates

        # Calculate numeric representation of dates relative to 1970-01-01
        epoch = datetime(1969, 12, 20)
        df["Date_Numeric"] = (df["Date"] - epoch).dt.days

        # Sort data in ascending order of dates
        df = df.sort_values(by="Date_Numeric", ascending=True).reset_index(drop=True)

        # Extract arrays for the output
        date_array = df["Date_Numeric"].tolist()
        value_array = df["Value"].tolist()

        # Format arrays as strings
        formatted_dates = ", ".join(map(str, date_array))
        formatted_values = ", ".join(map(str, value_array))

        # Combine the formatted array with the required suffix
        formatted_data = f"[[{formatted_dates}], [{formatted_values}], null, null, '', 1, []]"

        # Get the most recent date and value
        most_recent_date = df.iloc[-1]["Date"]
        most_recent_value = df.iloc[-1]["Value"]

        # Format the date into "4:00 PM EST, Fri Dec 13" format
        formatted_date = most_recent_date.strftime("4:00 PM EST, %a %b %d")
        formatted_value = f"{most_recent_value:,.2f}"
        
        # Append percentage change to the value
        formatted_value += formatted_percentage

        print("Step 2: Reading HTML file...")
        # Read the HTML content
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Step 3: Update the data section in HTML
        print("Step 3: Updating the data section in HTML...")
        data_marker = "<!-- TSX historical prices -->"
        if data_marker in html_content:
            data_start = html_content.find(data_marker) + len(data_marker)
            data_end = html_content.find("]]", data_start) + 2  # Locate the end of the array
            html_content = (
                html_content[:data_start] +
                "\n" +
                formatted_data +
                "\n" +
                html_content[data_end:]
            )
        else:
            print(f"Data section marker '{data_marker}' not found in HTML.")
            return

        # Step 4: Locate the specific section for S&P 500 Historical Prices
        print("Step 4: Updating the specific section for S&P 500 Historical Prices...")
        sp500_marker = '<a class=box href="/tsx-historical-prices">'
        marker_start = html_content.find(sp500_marker)
        if marker_start == -1:
            print("Marker for S&P 500 Historical Prices not found in the HTML.")
            return

        # Locate the end of this section
        section_end = html_content.find("</a>", marker_start) + 4
        section_content = html_content[marker_start:section_end]

        # Update the value <div> within this section
        value_start = section_content.find("<div>", section_content.find("<h3>")) + 5
        value_end = section_content.find("</div>", value_start)
        updated_section = (
            section_content[:value_start] +
            formatted_value +
            section_content[value_end:]
        )

        # Update the date <div> within this section
        date_marker = '<div class="date">'
        date_start = updated_section.find(date_marker) + len(date_marker)
        date_end = updated_section.find("</div>", date_start)
        updated_section = (
            updated_section[:date_start] +
            formatted_date +
            updated_section[date_end:]
        )

        # Replace the original section in the HTML
        html_content = (
            html_content[:marker_start] +
            updated_section +
            html_content[section_end:]
        )

        # Step 5: Save the updated HTML
        print("Step 5: Writing updated HTML to output file...")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"HTML file '{output_file}' updated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
html_file = './index.html'
excel_file = './data/tsx.xlsx'
output_file = './index.html'

# Run the update function
update_sp500_html(html_file, excel_file, output_file)
