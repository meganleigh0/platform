import openpyxl
import pandas as pd

# Load the workbook
wb = openpyxl.load_workbook('assets/DailyStatusArchivesAug2024.xlsx', data_only=True)

# Function to find rows where specific keywords appear
def find_row(ws, keyword):
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and keyword in str(cell.value):
                return cell.row
    return None

# Function to extract tables based on the header row found
def extract_table(ws, start_row, columns):
    data = []
    for row in ws.iter_rows(min_row=start_row+1, values_only=True):
        # Stop when the first empty row is encountered
        if all([cell is None for cell in row]):
            break
        data.append(row)
    
    df = pd.DataFrame(data, columns=columns)
    return df

# Create an empty list to store all tables
all_tables = []

# Iterate over each sheet in the workbook
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    
    # Find the row that contains the 'Station' identifier
    station_row = find_row(ws, 'Station')
    
    if station_row:
        # Assume headers are in the row after 'Station' keyword
        headers = ['Contract', 'MRP', 'Actual', 'Delta', 'Flow']
        
        # Extract data starting from this row
        station_df = extract_table(ws, station_row, headers)
        
        # Add a column to identify the station and date
        station_df['Station'] = sheet_name  # This will be the sheet name
        station_df['Date'] = ws.cell(row=station_row, column=2).value  # Adjust based on date location

        # Append to the list of all tables
        all_tables.append(station_df)

# Concatenate all station dataframes
full_df = pd.concat(all_tables, ignore_index=True)

# Display the final dataframe
print(full_df)