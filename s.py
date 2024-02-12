import pandas as pd


# Function to explode operations array into separate rows
def explode_ops(row):
    return pd.DataFrame(row['operations'], columns=['hours', 'description', 'department'])

# Explode operations
df = df.explode('operations').reset_index(drop=True)

# Group by station and assembly, and aggregate operations
result = df.groupby(['station', 'desc', 'mbomID', 'assemblyID']).agg({
    'operations': lambda x: x.tolist(),
    'total_ops': 'sum',
    'total_hours': 'sum'
}).reset_index()

print(result)