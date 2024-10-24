import os
import pandas as pd
import xlwings as xw

folder_path = 'DailyStatus'
data = []

# Define possible plants, sections, and stations (same as before)
# ... [keep your existing definitions here] ...

def process_sheet(sheet, date):
    # [Same as before, but adjust to read values from xlwings]
    data_entries = []
    current_plant = None
    current_section = None
    current_station = None
    collecting_summary = False
    collecting_vehicles = False
    summary_headers = ['Contract', 'MRP', 'Actual', 'Delta', 'Flow']
    summary_data = []
    vehicle_list = []

    # Read all data from the sheet into a list of lists
    values = sheet.range('A1').expand().value

    for row in values:
        row = [cell if cell is not None else '' for cell in row]
        row_upper = [str(cell).strip().upper() for cell in row]

        # [Same logic as before]
        # ... [keep your existing processing code here] ...

    return data_entries

app = xw.App(visible=False)
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(folder_path, filename)
        try:
            wb = xw.Book(filepath)
        except Exception as e:
            print(f"Error loading workbook {filename}: {e}")
            continue
        for sheet in wb.sheets:
            date = sheet.name  # Assuming sheet name is the date
            data.extend(process_sheet(sheet, date))
        wb.close()
app.quit()

# Convert the data list into a DataFrame
df = pd.DataFrame(data)
df.to_csv('consolidated_data.csv', index=False)