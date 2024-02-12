df = pd.DataFrame(data)

# Function to create DataFrame from operations list
def create_ops_df(ops_list, index):
    return pd.DataFrame(ops_list, columns=['hours', 'description', 'department']).assign(index=index)

# Concatenate DataFrames for each row
df = pd.concat([create_ops_df(row['operations'], index) for index, row in df.iterrows()], ignore_index=True)

print(df)