import pandas as pd

def find_station_indices(df, station_names):
    """
    Find the start and end indices for given station names within a DataFrame.
    
    Args:
    df (pd.DataFrame): DataFrame to search within.
    station_names (list): List of station names to find indices for.
    
    Returns:
    dict: Dictionary mapping each station name to a tuple (start_index, end_index).
    """
    indices = {}
    for station in station_names:
        try:
            start_index = df[df.apply(lambda x: x.str.contains(station, na=False, case=False)).any(axis=1)].index[0]
            # Look for the next station or end of DataFrame
            end_index = df[start_index+1:].apply(lambda x: x.isna().all(), axis=1).idxmax() + start_index
            indices[station] = (start_index, end_index)
        except:
            indices[station] = (None, None)  # If station not found
    return indices

def extract_data_by_station(df, station_indices):
    """
    Extracts summary and vehicle data based on the indices of each station.
    
    Args:
    df (pd.DataFrame): DataFrame containing the data.
    station_indices (dict): Dictionary of indices for each station.
    
    Returns:
    dict: Dictionary containing summary and vehicle data for each station.
    """
    station_data = {}
    for station, (start_idx, end_idx) in station_indices.items():
        if start_idx is not None and end_idx is not None:
            # Extracting the section for this station
            station_df = df.iloc[start_idx:end_idx]

            # Assuming summary ends at 'Total'
            total_row = station_df[station_df.apply(lambda x: x.str.contains('Total', na=False, case=False)).any(axis=1)].index[0]
            summary_df = station_df.iloc[:total_row + 1]
            summary_df.columns = station_df.iloc[0]
            summary_df = summary_df[1:]

            # Assuming vehicle data starts two rows after 'Total'
            vehicle_df = station_df.iloc[total_row + 2:]
            vehicle_df.reset_index(drop=True, inplace=True)
            vehicle_df = vehicle_df.transpose()
            vehicle_df.columns = vehicle_df.iloc[0]
            vehicle_df = vehicle_df[1:]

            station_data[station] = {'Summary': summary_df, 'Vehicles': vehicle_df}
        else:
            station_data[station] = {'Summary': pd.DataFrame(), 'Vehicles': pd.DataFrame()}
    
    return station_data

# Example usage:
df = pd.read_excel('path_to_your_excel_file.xlsx', header=None)  # Load your data
station_names = ['Turrets', 'Hulls', 'Armor']  # Example station names
indices = find_station