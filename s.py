import pandas as pd

# Load the Excel file, skipping the first row which contains the year headers and reading the next two rows
file_path = "path_to_your_excel_file.xlsx"
df = pd.read_excel(file_path, header=[0, 1])  # Use multi-level header to capture both years and months

# Step 1: Clean up the Family and Program data
# The first few rows in column A are blank, so we fill them down after identifying Families (all caps)
df['Family'] = df.iloc[:, 0].where(df.iloc[:, 0].str.isupper(), None)  # Families are in uppercase
df['Family'].ffill(inplace=True)  # Fill down Family names

# Step 2: Separate Programs from Family
df['Program'] = df.iloc[:, 0].where(~df.iloc[:, 0].str.isupper(), None)  # Programs are non-uppercase

# Step 3: Drop rows where 'Program' is still NaN, as these are Family header rows
df_programs = df.dropna(subset=['Program']).copy()

# Step 4: Reshape the month/year columns
# We'll melt the year/month columns into a long format with one row per Year/Month/Qty
df_melted = df_programs.melt(
    id_vars=['Family', 'Program', 'Status', 'Group Code', 'Data Source'],  # Adjust these as needed
    var_name=['Year', 'Month'],  # Column names from multi-level header
    value_name='Qty'
)

# Step 5: Clean up the Month abbreviations if needed (J, F, M, etc.)
month_mapping = {'J': 'January', 'F': 'February', 'M': 'March', 'A': 'April', 'M': 'May', 'J': 'June',
                 'J': 'July', 'A': 'August', 'S': 'September', 'O': 'October', 'N': 'November', 'D': 'December'}
df_melted['Month'] = df_melted['Month'].map(month_mapping)

# Step 6: Display the cleaned dataframe
print(df_melted.head())