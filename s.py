import pandas as pd
from openpyxl import load_workbook

# Load the Excel workbook and select the sheet
file_path = 'your_file.xlsx'
wb = load_workbook(file_path)
sheet = wb.active  # Assuming the first sheet is the one you want

# Extract the years and months
years = [cell.value for cell in sheet[1]]  # First row for years
months = [cell.value for cell in sheet[2]]  # Second row for months

# List to store the final records
records = []

# Iterate over the rows starting from the third row (where the programs and quantities are)
for row in sheet.iter_rows(min_row=3, values_only=True):
    program = row[0]  # Assuming Column A contains the program name
    
    if program:  # Skip empty rows in Column A
        for col_idx, quantity in enumerate(row[1:], start=1):  # Iterate over the remaining columns
            year = years[col_idx]
            month = months[col_idx]
            
            # If both year and month are available and the quantity is not None, create a record
            if year and month and quantity is not None:
                records.append({
                    'Program': program,
                    'Quantity': quantity,
                    'Year': year,
                    'Month': month
                })

# Convert the records into a pandas DataFrame
df = pd.DataFrame(records)

# Show the resulting DataFrame
print(df)