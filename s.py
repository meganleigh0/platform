import pandas as pd

def extract_summary_and_vehicle_data(df):
    """
    Extract summary and vehicle data for each program from a given section DataFrame.
    
    Args:
    df (pd.DataFrame): DataFrame containing data for a specific section.
    
    Returns:
    tuple: (summary DataFrame, detailed vehicle DataFrame)
    """
    # Drop completely empty columns to clean up the DataFrame
    df = df.dropna(how='all', axis=1).reset_index(drop=True)

    # Extracting summary table
    # Assuming summary ends at 'Total' which is unique in its column
    total_row = df[df.apply(lambda x: x.str.contains('Total', na=False, case=False)).any(axis=1)].index[0]
    summary_df = df.iloc[:total_row + 1]  # +1 to include the row with 'Total'
    summary_df.columns = df.iloc[0]  # Assuming first row is the header
    summary_df = summary_df[1:]  # Remove the header row from data

    # Extracting vehicle data
    vehicle_df = df.iloc[total_row + 2:]  # Assuming vehicle data starts two rows after 'Total'
    # Reset index for easier handling
    vehicle_df.reset_index(drop=True, inplace=True)

    # Vehicle data restructuring
    # Transpose the DataFrame to make each program's data a separate column
    vehicle_df = vehicle_df.transpose()
    # Assuming first row now has program identifiers after transposing
    vehicle_df.columns = vehicle_df.iloc[0]
    vehicle_df = vehicle_df[1:]  # Remove the program identifier row

    return summary_df, vehicle_df

# Example usage:
# Assuming you have a DataFrame 'section_df' from any section
# summary_data, vehicle_data = extract_summary_and_vehicle_data(section_df)
# print("Summary Data:")
# print(summary_data)
# print("\nVehicle Data:")
# print(vehicle_data)