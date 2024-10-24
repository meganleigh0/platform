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
        # Extract relevant data for this sheet using the section parser
        sheet_data = extract_sections_and_parse(ws, sheet_name)
        if sheet_data is not None:
            all_data.append(sheet_data)

    # Combine all sheet data into one DataFrame
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

# Function to extract specific sections and tables from the sheet
def extract_sections_and_parse(ws, sheet_name):
    sections = ["Station", "Contract", "MRP", "Actual", "Delta", "Flow"]

    data_list = []
    # Assuming stations like "Station", "Turret", "Hull", etc., are in your layout

    # Parse sections using key phrases from your station identifiers
    for section_name in sections:
        start_row = None
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
            if any(section_name in str(cell.value) for cell in row):
                start_row = row[0].row
                break

        if start_row is not None:
            # Extract data from the section starting at `start_row`
            section_data = []
            for row in ws.iter_rows(min_row=start_row + 1, max_row=ws.max_row, values_only=True):
                if any(row):
                    section_data.append(row)
                else:
                    break  # Stop on the first empty row
            
            # Create a DataFrame for the section
            df = pd.DataFrame(section_data, columns=['Contract', 'MRP', 'Actual', 'Delta', 'Flow'])
            df['Station'] = section_name
            df['Date'] = sheet_name.split()[0]  # Adjust date extraction based on sheet name
            data_list.append(df)

    # Combine all section data
    return pd.concat(data_list, ignore_index=True) if data_list else None

# Function to handle all workbooks in the "DailyStatusFolder"
def load_all_workbooks(directory_path):
    all_data = []

    # Loop through all subfolders (each month) in the DailyStatusFolder
    for month_folder in os.listdir(directory_path):
        month_folder_path = os.path.join(directory_path, month_folder)

        # Ensure we're only processing folders
        if os.path.isdir(month_folder_path):
            # Loop through each Excel file in the month's folder
            for file_name in os.listdir(month_folder_path):
                if file_name.endswith('.xlsx'):
                    file_path = os.path.join(month_folder_path, file_name)
                    workbook_data = load_workbook_data(file_path)
                    if not workbook_data.empty:
                        all_data.append(workbook_data)

    # Combine all data from all workbooks into one DataFrame
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

# Example usage
directory = "DailyStatusFolder"  # Your folder with the daily reports
final_data = load_all_workbooks(directory)

# Display the final aggregated data
print(final_data)