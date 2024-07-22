 Find indices of headers for Teardown and Machinging
    teardown_index = data_df[data_df.apply(lambda row: row.str.contains('Teardown', na=False)).any(axis=1)].index[0]
    maching_index = data_df[data_df.apply(lambda row: row.str.contains('Machinging', na=False)).any(axis=1)].index[0]

    # Split the dataframe into two parts for each station
    teardown_df = data_df.iloc[teardown_index:maching_index].dropna(axis=1, how='all')
    maching_df = data_df.iloc[maching_index:end_row].dropna(axis=1, how='all')

    # Clean and reformat the data frames if necessary
    # Here you would include steps to rename columns, drop unnecessary rows, etc.
    # Example:
    teardown_df.columns = ['Contract', 'MRP', 'Actual', 'Delta', 'Flow']
    maching_df.columns = ['Contract', 'MRP', 'Actual', 'Delta', 'Flow']

    # Return the cleaned data
    return teardown_df, maching_df

# Example usage:
teardown_data, maching_data = read_status_report('path_to_your_file.xlsx')
print("Teardown Data:")
print(teardown_data)
print("\nMaching Data:")
print(maching_data)
