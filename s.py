import pandas as pd
from openpyxl import load_workbook

# Load the workbook and select the correct sheet
file_path = '/mnt/data/your_file.xlsx'  # Update this path with your actual file location
wb = load_workbook(file_path)
sheet = wb.active  # Assuming the data is in the first sheet

# Extract years and months - ensuring we capture all columns correctly
years = [cell.value for cell in sheet[1][4:]]  # Years start from column E (index 4)
months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']  # Static months list

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
        # Iterate over the columns starting from column E, but now we account for 12 months under each year
        for year_idx in range(4, len(row), 12):  # Step by 12 columns (12 months per year)
            year = years[year_idx - 4]  # Match the year from the years list
            
            # Now loop over the next 12 columns for each month
            for month_offset in range(12):
                col_idx = year_idx + month_offset
                quantity = row[col_idx].value  # Extract the quantity
                
                # If quantity exists, create a record
                if year and months[month_offset] and quantity is not None:
                    records.append({
                        'Program': program,
                        'Status': status,
                        'Group Code': group_code,
                        'Data Source': data_source,
                        'Year': year,
                        'Month': months[month_offset],
                        'Quantity': quantity
                    })

# Convert the list of records into a pandas DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)