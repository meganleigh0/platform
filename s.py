import pandas as pd

# Assuming df is your DataFrame

# Adjusting functions to convert hours from strings to floats
def sum_operations(operations):
    # Convert hours to float and sum them
    return sum(float(op[0]) for op in operations if isinstance(op, list) and len(op) > 0 and isinstance(op[0], str))

def longest_operation(operations):
    # Convert hours to float, then find the operation with the maximum hours
    valid_operations = [(float(op[0]), op[1], op[2]) for op in operations if isinstance(op, list) and len(op) > 2 and isinstance(op[0], str)]
    if valid_operations:
        return max(valid_operations, key=lambda x: x[0])
    return []

# Applying the updated functions
df['TotalHours'] = df['Operations'].apply(sum_operations)
df['LongestOperation'] = df['Operations'].apply(longest_operation)

# Show the updated DataFrame
print(df[['MbomID', 'PartNumber', 'Station', 'TotalHours', 'LongestOperation']])