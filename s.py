import pandas as pd
from openpyxl import load_workbook

# Load the workbook and select the correct sheet
file_path = '/mnt/data/your_file.xlsx'
wb = load_workbook(file_path)
sheet = wb.active  # Assuming the data is in the first sheet

# Extract years and months starting from column E (which is index 4)
years = [cell.value for cell in sheet[1][4:]]  # First row for years
months = [cell.value for cell in sheet[2][4:]]  # Second row for months

# List to store the final records
records = []

# Iterate over the rows starting from the fourth row (where the program details and quantities start)
for row in sheet.iter_rows(min_row=4):
    program = row[0].value  # Program name from column A
    status = row[1].value   # Status from column B
    group_code = row[2].value  # Group Code from column C
    data_source = row[3].value  # Data Source from column D
    
    # Skip rows where there is no program name
    if program:
        # Iterate over the remaining columns starting from column E (index 4) for quantities
        for col_idx, cell in enumerate(row[4:], start=4):
            quantity = cell.value
            year = years[col_idx - 4]
            month = months[col_idx - 4]
            
            # Create a record if the quantity is not None
            if year and month and quantity is not None:
                records.append({
                    'Program': program,
                    'Status': status,
                    'Group Code': group_code,
                    'Data Source': data_source,
                    'Year': year,
                    'Month': month,
                    'Quantity': quantity
                })

# Convert the list of records into a pandas DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)