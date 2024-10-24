# Step 1: Forward Fill the Year Column
df['Year'] = df['Year'].fillna(method='ffill')

# Step 2: Map Months to Full Names
month_mapping = {
    'J': 'January',
    'F': 'February',
    'M': 'March',
    'A': 'April',
    'M': 'May',
    'J': 'June',
    'J': 'July',
    'A': 'August',
    'S': 'September',
    'O': 'October',
    'N': 'November',
    'D': 'December'
}

# Apply the month mapping
df['Month'] = df['Month'].map(month_mapping)

# Display the DataFrame
print(df)