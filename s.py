df = pd.DataFrame(data)

# Function to flatten operations list
def flatten_ops(row):
    return pd.DataFrame(row['operations'], columns=['hours', 'description', 'department'])

# Apply the function to each row
df = df.join(df.apply(flatten_ops, axis=1))

# Drop the original operations column
df.drop(columns=['operations'], inplace=True)

print(df)