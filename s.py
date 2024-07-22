# First, let's identify the starting indices of each station within the "Tops" section
station_names = ['Teardown', 'Machinging', 'Armor', 'Appur', 'Paint']
station_indices = {name: tops_data[tops_data['Plant Status'].str.contains(name, na=False)].index.min() for name in station_names}
station_indices['Bottoms'] = bottoms_index  # To define the end of the last station

# Now let's define a function to process each station's table
def process_station_data(start_index, end_index, data):
    # Extract data for the current station
    station_data = data.iloc[start_index:end_index]
    # Assume the first row after the station name is the header
    header = station_data.iloc[0]
    station_data = station_data.iloc[1:]
    station_data.columns = header.values
    station_data = station_data.dropna(axis=1, how='all').dropna(axis=0, how='all')  # Clean up the table
    return station_data

# Process each station's data using the identified indices
station_tables = {}
for i, (name, start_index) in enumerate(station_indices.items()):
    if i < len(station_indices) - 1:  # Ensure we do not go out of bounds
        next_station_name = list(station_indices.keys())[i + 1]
        end_index = station_indices[next_station_name]
        station_tables[name] = process_station_data(start_index, end_index, tops_data)

# Display an example station table, e.g., 'Teardown'
station_tables['Teardown'].head()
