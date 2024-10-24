import pandas as pd

# Step 1: Load the Excel file without any headers
file_path = "path_to_your_excel_file.xlsx"  # Replace with actual path
df = pd.read_excel(file_path, header=None)  # No header

# Step 2: Manually assign column names
# Assuming the first two rows are year and month, followed by the data
year_row = df.iloc[0]
month_row = df.iloc[1]
columns = ['Program', 'Status', 'Group Code', 'Data Source'] + [f'{year}_{month}' for year, month in zip(year_row, month_row)]
df.columns = columns

# Step 3: Remove the first two rows (year and month rows)
df = df.drop([0, 1]).reset_index(drop=True)

# Step 4: Identify Family rows (all caps, no numbers)
df['Is_Family'] = df['Program'].apply(lambda x: x.isupper() and not any(char.isdigit() for char in x))

# Step 5: Fill down Family names
df['Family'] = df.loc[df['Is_Family'], 'Program']
df['Family'].ffill(inplace=True)

# Step 6: Filter out the Family rows from the data
df_filtered = df[~df['Is_Family']].copy()

# Step 7: Reshape the month/year columns into a long format
month_columns = columns[4:]  # All columns after 'Data Source'
df_melted = df_filtered.melt(
    id_vars=['Family', 'Program', 'Status', 'Group Code', 'Data Source'],
    value_vars=month_columns,
    var_name='Year_Month',
    value_name='Quantity'
)

# Step 8: Split the 'Year_Month' into separate 'Year' and 'Month' columns
df_melted[['Year', 'Month']] = df_melted['Year_Month'].str.split('_', expand=True)

# Step 9: Output the cleaned dataframe
print(df_melted.head())