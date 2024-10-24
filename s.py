import os
import pandas as pd
import xlwings as xw

# Define the folder path where the Excel files are stored
folder_path = 'DailyStatus'  # Update this path if your folder is named differently

# Initialize an empty list to store the data
data = []

# Define possible plants, sections, and stations
plants = ['Plant 1', 'Plant 3', 'T&A', 'TNA', 'Test and Accept']
sections = {
    'P1 Turrets': ['Machining', 'Armor Install', 'Appurtenance', 'Paint'],
    'P1 Hull': ['Armor', 'Structure', 'Appurtenance', 'Paint'],
    'P3 Turrets': ['Station 0', 'Station 1', 'Stations 2-3-4', 'Stations 5-6'],
    'P3 Hull': ['Station 0', 'Station 1', 'Stations 2-3-4', 'Stations 5-6'],
    'T&A': ['Test and Accept', 'Final Paint', 'Prep and Ship'],
    'TNA': ['Test and Accept', 'Final Paint', 'Prep and Ship']
}

# Flatten lists of sections and stations
all_sections = list(sections.keys())
all_stations = [station for stations in sections.values() for station in stations]

def process_sheet(sheet, date):
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
    values = sheet.used_range.value

    if values is None:
        return data_entries  # Skip empty sheets

    for row in values:
        # Ensure row is a list
        if not isinstance(row, list):
            row = [row]
        row = [cell if cell is not None else '' for cell in row]
        row_upper = [str(cell).strip().upper() for cell in row]

        # Identify plant
        if any(plant.upper() in row_upper for plant in plants):
            current_plant = next(plant for plant in plants if plant.upper() in row_upper)
            current_section = current_station = None
            collecting_summary = collecting_vehicles = False
            continue

        # Identify section
        if any(section.upper() in row_upper for section in all_sections):
            current_section = next(section for section in all_sections if section.upper() in row_upper)
            current_station = None
            collecting_summary = collecting_vehicles = False
            continue

        # Identify station
        if any(station.upper() in row_upper for station in all_stations):
            current_station = next(station for station in all_stations if station.upper() in row_upper)
            collecting_summary = collecting_vehicles = False
            continue

        # Identify summary table headers
        if set([header.upper() for header in summary_headers]).issubset(set(row_upper)):
            collecting_summary = True
            summary_data = []
            continue

        # Collect summary table data
        if collecting_summary:
            if any(row):
                summary_row = dict(zip(summary_headers, row))
                summary_data.append(summary_row)
            else:
                collecting_summary = False
                collecting_vehicles = True
            continue

        # Collect vehicle list
        if collecting_vehicles:
            cell_value = str(row[0]).strip()
            if cell_value.upper() in ['M DAYS', 'PLANNED WIP', '']:
                collecting_vehicles = False
                data_entries.append({
                    'Plant': current_plant,
                    'Section': current_section,
                    'Station': current_station,
                    'Summary Table': summary_data,
                    'Vehicle List': vehicle_list,
                    'Date': date
                })
                vehicle_list = []
            else:
                vehicle_list.append(cell_value)
    return data_entries

# Create an instance of the Excel application
app = xw.App(visible=False)
# Suppress Excel alerts
app.display_alerts = False
app.screen_updating = False

for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(folder_path, filename)
        try:
            # Open the workbook with parameters to suppress prompts
            wb = app.books.open(
                filepath,
                ReadOnly=True,
                IgnoreReadOnlyRecommended=True,
                UpdateLinks=False
            )
        except Exception as e:
            print(f"Error loading workbook {filename}: {e}")
            continue
        for sheet in wb.sheets:
            date = sheet.name  # Assuming sheet name is the date
            try:
                data.extend(process_sheet(sheet, date))
            except Exception as e:
                print(f"Error processing sheet {sheet.name} in workbook {filename}: {e}")
                continue
        wb.close()
app.quit()

# Convert the data list into a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Optional: Save the DataFrame to a CSV file for verification
df.to_csv('consolidated_data.csv', index=False)