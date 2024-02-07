import pandas as pd

# Sample DataFrame creation - replace this with your actual DataFrame loading method
data = {
    'MbomID': [1, 2],
    'PartNumber': ['P1', 'P2'],
    'Name': ['Part 1', 'Part 2'],
    'Station': ['S1', 'S2'],
    'Operations': [
        [[1.5, 'Op 1', 'Dept 1'], [2, 'Op 2', 'Dept 2']],
        0  # Assuming 0 means no operations for simplicity
    ]
}
df = pd.DataFrame(data)

# Ensure Operations is a list of lists, not 0, for consistency
df['Operations'] = df['Operations'].apply(lambda x: x if x != 0 else [])

# Sum of operations by Station and Assembly
def sum_operations(operations):
    return sum(op[0] for op in operations)

df['TotalHours'] = df['Operations'].apply(sum_operations)
sum_by_station_assembly = df.groupby(['Station', 'PartNumber'])['TotalHours'].sum().reset_index()

# Longest operation
def longest_operation(operations):
    if operations:
        return max(operations, key=lambda x: x[0])
    return []

df['LongestOperation'] = df['Operations'].apply(longest_operation)

# For parallelization analysis, you might want to explore operations within each station and assembly
# that have significant hours and see if they belong to different departments, indicating potential for parallel work.

print("Sum of Operations by Station and Assembly:")
print(sum_by_station_assembly)

print("\nDataFrame with Longest Operation:")
print(df[['MbomID', 'PartNumber', 'Station', 'LongestOperation']])