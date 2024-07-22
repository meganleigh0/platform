# Assuming 'Teardown' starts right after the 'Tops' marker, and ends before a blank row or next section marker
# Find the start index for 'Teardown'
teardown_start_index = tops_index + 1  # The row after 'Tops' is the header for 'Teardown'

# Find the end index for 'Teardown' by locating the first blank row or the start of the next section
teardown_end_index = tops_data[tops_data.isnull().all(axis=1)].index[0] if not tops_data[tops_data.isnull().all(axis=1)].empty else tops_data.index[-1]

# Extract 'Teardown' data
teardown_data = tops_data.loc[teardown_start_index:teardown_end_index]

# Assuming the row right after 'Teardown' header row is the header for the table
teardown_header = teardown_data.iloc[0]
teardown_table = teardown_data.iloc[1:]

# Set the correct header
teardown_table.columns = teardown_header.values

# Clean up the data table by dropping NaN columns and rows that are entirely NaN
teardown_table_cleaned = teardown_table.dropna(axis=1, how='all').dropna(axis=0, how='all')

# Show the cleaned table for 'Teardown'
teardown_table_cleaned
