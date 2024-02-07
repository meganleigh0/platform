import pandas as pd

# Assuming df is your DataFrame

# Correct the function name and implementation
def sum_operations(operations):
    # Check if operations is not empty and is a list
    if operations and isinstance(operations, list):
        return sum(op[0] for op in operations if isinstance(op, list) and len(op) > 0 and isinstance(op[0], (int, float)))
    return 0

# Apply the corrected function
df['TotalHours'] = df['Operations'].apply(sum_operations)

# Now, let's correct the part for finding the longest operation
def longest_operation(operations):
    # Filter out valid operations and find the one with the longest duration
    valid_operations = [op for op in operations if isinstance(op, list) and len(op) > 0 and isinstance(op[0], (int, float))]
    if valid_operations:
        return max(valid_operations, key=lambda x: x[0])
    return []

df['LongestOperation'] = df['Operations'].apply(longest_operation)

# Display the modified DataFrame
print(df[['MbomID', 'PartNumber', 'Station', 'TotalHours', 'LongestOperation']])