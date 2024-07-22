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
    # Clean DataFrame by dropping all-NaN columns
    df = df.dropna(how='all', axis=1).reset_index(drop=True)

    # Find 'Total' to split summary and vehicle data
    total_index = df.index[df.apply(lambda x: 'Total' in x.values, axis=1)][0]

    # Extract summary data
    summary_df = df.iloc[:total_index + 1]
    summary_df.columns = summary_df.iloc[0]  # Setting the first row as header
    summary_df = summary_df[1:].reset_index(drop=True)

    # Extract vehicle data starting after 'Total'
    vehicle_df = df.iloc[total_index + 1:].reset_index(drop=True)
    vehicle_df = vehicle_df.transpose()
    headers = vehicle_df.iloc[0]  # Grabbing the first row as headers after transpose
    vehicle_df = vehicle_df[1:].reset_index(drop=True)
    vehicle_df.columns = headers  # Setting proper headers

    # Structured DataFrame for vehicle data
    structured_vehicles = pd.DataFrame()

    for program in vehicle_df.columns:
        # Constructing a DataFrame for each program's vehicles
        program_df = vehicle_df[[program]].dropna().reset_index()
        program_df.rename(columns={'index': 'Vehicle', program: 'Quantity'}, inplace=True)
        program_df['Station'] = station_name
        program_df['Program'] = program
        # Concatenate using 'ignore_index' to handle index alignment
        structured_vehicles = pd.concat([structured_vehicles, program_df], ignore_index=True)

    return summary_df, structured_vehicles

# Example usage:
# Load your DataFrame 'p1_turret' and use 'Turrets' as the station name
summary_data, vehicle_data = extract_summary_and_vehicle_data(p1_turret, 'Turrets')
print("Summary Data:")
print(summary_data)
print("\nVehicle Data:")
print(vehicle_data)