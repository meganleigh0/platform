import pandas as pd

# Load the Excel file
file_path = "path_to_your_file.xlsx"  # Replace with the actual file path
df = pd.read_excel(file_path, skiprows=3)  # Skip the first 3 rows which are empty

# Fill down the 'Family' column
df['Family'] = df['A'].fillna(method='ffill')

# Filter out any rows that do not contain a program
df_filtered = df.dropna(subset=['Program'])

# Reshape the month/year columns into a long format
df_melted = df_filtered.melt(
    id_vars=['Family', 'Program', 'Status', 'Group Code', 'Source'], 
    var_name='Month/Year', 
    value_name='Quantity'
)

# Display the cleaned and reshaped data
print(df_melted.head())