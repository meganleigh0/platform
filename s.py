import pandas as pd

def extract_summary_and_vehicle_data(df):
    """
    Extract summary and vehicle data for each program from a given section DataFrame.

    Args:
    df (pd.DataFrame): DataFrame containing data for a specific section.

    Returns:
    tuple: (summary DataFrame, detailed vehicle DataFrame)
    """
    # Reset index for easier slicing
    df.reset_index(drop=True, inplace=True)

    # Drop completely empty columns to clean up the DataFrame
    df = df.dropna(how='all', axis=1)

    # Finding the row index for 'Total' which marks the end of the summary data
    total_index = df.index[df.apply(lambda x: 'Total' in x.values, axis=1)].tolist()[0]

    # Extract summary data
    summary_df = df.iloc[:total_index + 1]
    summary_df.columns = summary_df.iloc[0]  # Set the first row as column header
    summary_df = summary_df[1:]  # Drop the first row since it's now the header

    # Extract vehicle data
    vehicle_data_start_index = total_index + 1
    vehicle_df = df.iloc[vehicle_data_start_index:]
    
    # Assume that the first non-empty row contains program names as headers
    header_row = vehicle_df.dropna(how='all', axis=1).iloc[0]
    vehicle_df.columns = header_row.values
    vehicle_df = vehicle_df[1:]  # Remove the header row

    return summary_df, vehicle_df

# Example usage:
# Assuming 'p1_turret' is your DataFrame loaded with the appropriate data
summary_data, vehicle_data = extract_summary_and_vehicle_data(p1_turret)
print("Summary Data:")
print(summary_data)
print("\nVehicle Data:")
print(vehicle_data)