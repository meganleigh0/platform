import pandas as pd

# Sample DataFrame for demonstration; replace with your actual data loading
data = {
    'MbomID': [1, 2],
    'PartNumber': ['P1', 'P2'],
    'Name': ['Part 1', 'Part 2'],
    'Station': ['S1', 'S2'],
    'Operations': [
        [[1.5, 'Op 1', 'Dept 1'], [2, 'Op 2', 'Dept 2']],
        []  # Assuming empty list for no operations
    ]
}
df = pd.DataFrame(data)

# Ensuring Operations is a list of lists, or an empty list
df['Operations'] = df['Operations'].apply(lambda x: x if isinstance(x, list) else [])

def sum_operations(operations):
    # Sum only the hours (first element of each sub-array) from operations
    return sum(op[0] for op in operations if isinstance(op, list) and len(op) > 0 and isinstance(op[0], (int, float)))

df['TotalHours'] = df['Operations'].apply(sum_operations)

def longest_operation(operations):
    # Find the operation with the maximum hours
    if not operations or not isinstance(operations, list):
        return []
    # Filter to ensure we only process correctly structured operations
    filtered_ops = [op for op in operations if isinstance(op, list) and len(op) > 3 and isinstance(op[0], (int, float))]
    if not filtered_ops:
        return []
    return max(filtered_ops, key=lambda x: x[0])

df['LongestOperation'] = df['Operations'].apply(longest_operation)

# Show the updated DataFrame
print(df[['MbomID', 'PartNumber', 'Station', 'TotalHours', 'LongestOperation']])