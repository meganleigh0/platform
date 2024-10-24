import openpyxl
import pandas as pd
import os

# Function to load a workbook and extract data from each sheet
def load_workbook_data(file_path):
    # Load the Excel workbook using openpyxl
    wb = openpyxl.load_workbook(file_path, data_only=True)

    all_data = []

    # Loop through each sheet (each day) in the workbook
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]

        # Extract relevant data for this sheet
        sheet_data = extract_data_from_sheet(ws, sheet_name)

        if sheet_data is not None:
            all_data.append(sheet_data)

    # Combine all sheet data into one DataFrame
    return pd.concat(all_data, ignore_index=True)

# Function to extract data from an individual sheet
def extract_data_from_sheet(ws, sheet_name):
    # Try to identify the section in the sheet, locate station headers and pull relevant rows
    start_row = None
    station_data = []

    # Search for station headers or key identifiers (adjust based on your specific needs)
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        if any('Station' in str(cell.value) for cell in row):
            start_row = row[0].row
            break
    
    if start_row is None:
        return None  # No station data found in this sheet

    # Extract the rows following the station header
    for row in ws.iter_rows(min_row=start_row + 1, max_row=ws.max_row, values_only=True):
        # Check if this row has relevant data (adjust according to your data structure)
        if any(row):
            station_data.append(row)
        else:
            break  # Stop at the first empty row

    # Convert the extracted data into a DataFrame
    columns = ['Contract', 'MRP', 'Actual', 'Delta', 'Flow', 'Station', 'Date']
    df = pd.DataFrame(station_data, columns=columns[:len(station_data[0])])

    # Add the station name (from sheet name) and date (extracted from the workbook structure)
    df['Station'] = sheet_name
    df['Date'] = sheet_name.split()[0]  # Adjust this based on how the date is stored in the sheet name

    return df

# Function to handle all workbooks in a directory
def load_all_workbooks(directory_path):
    all_data = []

    # Loop through all Excel files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(directory_path, file_name)
            workbook_data = load_workbook_data(file_path)
            all_data.append(workbook_data)

    # Combine all data from all workbooks into one DataFrame
    return pd.concat(all_data, ignore_index=True)

# Example usage
directory = "path_to_directory_containing_excel_files"
final_data = load_all_workbooks(directory)

# Display the final aggregated data
print(final_data)