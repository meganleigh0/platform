import pandas as pd
from openpyxl import load_workbook

# Load the workbook and select the correct sheet
file_path = '/mnt/data/your_file.xlsx'
wb = load_workbook(file_path)
sheet = wb.active  # Assuming the data is in the first sheet

# Extract years and months
years = [cell.value for cell in sheet[1][4:]]  # Years start from column E (index 4)
months = [cell.value for cell in sheet[2][4:]]  # Months are in the second row, starting from column E

# List to hold the final records
records = []

# Iterate over the rows, starting from the third row (where the program details and quantities start)
for row in sheet.iter_rows(min_row=4, values_only=True):
    program = row[0]  # Program name from column A
    status = row[1]   # Status from column B
    group_code = row[2]  # Group Code from column C
    data_source = row[3]  # Data Source from column D
    
    if program:  # Skip empty rows where there is no program
        for col_idx, quantity in enumerate(row[4:], start=4):  # Start from column E (index 4)
            year = years[col_idx - 4]
            month = months[col_idx - 4]
            
            # If quantity is not None, create a record
            if quantity is not None:
                records.append({
                    'Program': program,
                    'Status': status,
                    'Group Code': group_code,
                    'Data Source': data_source,
                    'Year': year,
                    'Month': month,
                    'Quantity': quantity
                })

# Convert the list of records into a DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)