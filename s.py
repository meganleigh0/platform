
# Initialize a list to collect data from each station
daily_dfs = []

# Define a function to search for specific terms (like 'MRP', 'Actual') and extract rows accordingly
def extract_station_data(sheet_name, header_labels, station_name):
    # Parse the sheet
    df = daily_status.parse(sheet_name, header=None)
    
    # Find the first occurrence of the header labels to determine where the data starts
    header_row = df[df.apply(lambda row: row.astype(str).str.contains('|'.join(header_labels)).any(), axis=1)].index[0]
    
    # Extract data starting from that row
    station_data = df.loc[header_row:, :]
    
    # Clean up the station_data
    station_data.columns = station_data.iloc[0]  # Set headers
    station_data = station_data.drop(station_data.index[0])  # Drop the header row
    
    # Add a Station and Date column
    station_data['Station'] = station_name
    station_data['Date'] = pd.to_datetime(sheet_name.split('Abrams ')[1].replace(' ', '').replace('.', '/'))
    
    return station_data

# Define your stations and the labels to search for in the sheet
stations = [
    {'name': 'Turret Station 0', 'sheet_index': 0},
    {'name': 'Turret Station 1', 'sheet_index': 1},
    {'name': 'Turret Station 2/3/4', 'sheet_index': 2},
    # Add more stations as needed...
]

header_labels = ['MRP', 'Actual', 'Delta', 'Flow']

# Loop over the stations and extract their data
for station in stations:
    sheet_name = daily_status.sheet_names[station['sheet_index']]
    daily_dfs.append(extract_station_data(sheet_name, header_labels, station['name']))

# Concatenate all data
daily_df = pd.concat(daily_dfs, ignore_index=True)
print(daily_df)

# Clean NaN values in important columns
daily_df.dropna(subset=['MRP', 'Actual', 'Delta', 'Flow'], inplace=True)

# You can also fill NaNs if the data is consistent but incomplete
daily_df.fillna(method='ffill', inplace=True)  # Forward fill for missing values

# You can also apply custom transformations to correct any specific inconsistencies