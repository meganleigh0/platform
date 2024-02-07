def flatten_operations_by_station(df, station):
    """
    Flatten all operations for a given station into a single list.

    Parameters:
    - df: DataFrame containing your data.
    - station: The station for which operations should be flattened.

    Returns:
    - A flattened list of all operations for the given station.
    """
    # Filter the DataFrame by the specified station
    filtered_df = df[df['Station'] == station]

    # Extract the operations column and flatten it
    operations_list = filtered_df['Operations'].tolist()
    flattened_operations = [op for sublist in operations_list for op in sublist if isinstance(sublist, list)]

    return flattened_operations

# Sample usage:
station = 'S1'  # Example station
flattened_operations = flatten_operations_by_station(df, station)

# Display the flattened list of operations
print(f"Flattened operations for station {station}:")
print(flattened_operations)