
# Function to create DataFrame from operations list with additional columns
def create_ops_df(ops_list, index, station, mbomID, description):
    ops_df = pd.DataFrame(ops_list, columns=['hours', 'description', 'department'])
    ops_df['index'] = index
    ops_df['station'] = station
    ops_df['mbomID'] = mbomID
    ops_df['description'] = description
    return ops_df

# Concatenate DataFrames for each row
df = pd.concat([create_ops_df(row['operations'], index, row['station'], row['mbomID'], row['desc']) for index, row in df.iterrows()], ignore_index=True)

print(df)