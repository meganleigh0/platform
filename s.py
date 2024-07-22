import pandas as pd

def process_p1_turret_data(df):
    # Find all unique station names in the first row (ignoring NaN values)
    station_names = df.iloc[0].dropna().unique()
    
    # Dictionary to hold dataframes for each station
    station_data = {name: pd.DataFrame() for name in station_names}
    
    # Process each station
    for station in station_names:
        # Get all column indices for the current station
        cols = df.columns[df.iloc[0] == station].tolist()
        
        # Extract data for the current station
        station_df = df[cols]
        
        # Find the row index for 'Total' which demarcates summary from vehicle data
        total_idx = station_df[station_df.iloc[:, 0] == 'Total'].index.min()
        
        # Summary data includes rows up to and including the 'Total' row
        summary_df = station_df.iloc[:total_idx + 1]
        
        # Vehicle data includes rows after the 'Total' row
        vehicle_df = station_df.iloc[total_idx + 1:]
        
        # Store in dictionary
        station_data[station] = (summary_df, vehicle_df)
    
    return station_data

# Load your DataFrame here
# df = pd.read_csv('path_to_your_csv.csv')

# Assuming 'df' is your DataFrame loaded correctly
processed_data = process_p1_turret_data(df)

# Example to display data for a specific station
for station, (summary, vehicles) in processed_data.items():
    print(f"Station: {station}")
    print("Summary Data:")
    print(summary)
    print("Vehicle Data:")
    print(vehicles)
    print("\n")