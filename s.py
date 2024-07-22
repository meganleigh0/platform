import pandas as pd

def extract_summary_and_vehicle_data(df, station_name):
    """
    Extract summary and vehicle data for each program from a given section DataFrame.
    
    Args:
    df (pd.DataFrame): DataFrame containing data for a specific section.
    station_name (str): Name of the station to which the data belongs.

    Returns:
    tuple: (summary DataFrame, detailed vehicle DataFrame)
    """
    # Ensure the DataFrame is cleaned of all-NaN columns for accurate processing
    df = df.dropna(how='all', axis=1).reset_index(drop=True)

    # Find the 'Total' row to distinguish summary from vehicle data
    total_index = df.index[df.apply(lambda x: 'Total' in x.values, axis=1)][0]

    # Extract summary data
    summary_df = df.iloc[:total_index + 1]
    summary_df.columns = summary_df.iloc[0]  # Set the first row as header
    summary_df = summary_df[1:].reset_index(drop=True)  # Reset index after dropping header row

    # Extract vehicle data starting after 'Total'
    vehicle_df = df.iloc[total_index + 1:].reset_index(drop=True)
    vehicle_df = vehicle_df.transpose()
    headers = vehicle_df.iloc[0]  # The first row of transposed data as headers
    vehicle_df = vehicle_df[1:].reset_index(drop=True)
    vehicle_df.columns = headers  # Set proper headers

    # Create structured DataFrame for vehicles
    structured_vehicles = pd.DataFrame()

    # Process each column (program)
    for program in vehicle_df.columns:
        # Create a temporary DataFrame for each program
        temp_df = vehicle_df[[program]].dropna()
        temp_df = temp_df.reset_index()
        temp_df.rename(columns={'index': 'Vehicle', program: 'Quantity'}, inplace=True)
        temp_df['Station'] = station_name
        temp_df['Program'] = program
        structured_vehicles = pd.concat([structured_vehicles, temp_df], ignore_index=True)

    return summary_df, structured_vehicles

# Example usage:
# Assuming 'p1_turret' is your DataFrame loaded with the appropriate data and 'Turrets' is the station name
summary_data, vehicle_data = extract_summary_and_vehicle_data(p1_turret, 'Turrets')
print("Summary Data:")
print(summary_data)
print("\nVehicle Data:")
print(vehicle_data)