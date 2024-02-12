df = pd.DataFrame(data)

# Function to flatten operations list
def flatten_ops(row):
    ops_df = pd.DataFrame(row['operations'], columns=['hours', 'description', 'department'])
    ops_df['index'] = row.name  # Add a unique index to align with the main DataFrame
    return ops_df

# Apply the function to each row
df = df.join(df.apply(flatten_ops, axis=1))

# Drop the original operations column
df.drop(columns=['operations'], inplace=True)

print(df)