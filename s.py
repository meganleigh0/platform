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

# Adjust the function for longest operation to return a formatted string
def longest_operation_formatted(operations):
    valid_operations = [(float(op[0]), op[1], op[2]) for op in operations if isinstance(op, list) and len(op) > 2 and isinstance(op[0], str)]
    if valid_operations:
        longest_op = max(valid_operations, key=lambda x: x[0])
        return f"{longest_op[1]} - {longest_op[0]} Hours - {longest_op[2]}"
    return "N/A"

df['LongestOperationFormatted'] = df['Operations'].apply(longest_operation_formatted)
import matplotlib.pyplot as plt

# Group by Station and PartNumber for the sum of TotalHours
grouped_data = df.groupby(['Station', 'PartNumber'])['TotalHours'].sum().reset_index()

# Creating the bar chart
plt.figure(figsize=(10, 6))
for _, row in grouped_data.iterrows():
    plt.bar(f"{row['Station']}-{row['PartNumber']}", row['TotalHours'], label=f"{row['Station']}-{row['PartNumber']}")

plt.xlabel('Station-Assembly')
plt.ylabel('Total Hours')
plt.title('Total Hours of Operations by Station and Assembly')
plt.xticks(rotation=45)
plt.legend(title='Station-Assembly')
plt.tight_layout()
plt.show()