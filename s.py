import pandas as pd

# Load the Excel file with the first row being years and second row being months
file_path = "path_to_your_excel_file.xlsx"
df = pd.read_excel(file_path, header=[0, 1])  # Header has two levels for years and months

# Step 1: Extract the Family and Program information
# Assume column 0 contains both Family (uppercase, no numbers) and Programs (non-uppercase or containing numbers)
df['Family'] = df.iloc[:, 0].where(df.iloc[:, 0].str.isupper() & df.iloc[:, 0].str.contains(r'^\D+$'), None)
df['Family'].ffill(inplace=True)  # Fill down the family names
df['Program'] = df.iloc[:, 0].where(~df.iloc[:, 0].str.isupper() & df.iloc[:, 0].str.contains(r'^\D+$'), None)

# Step 2: Remove rows that are Family names since they are captured in the 'Family' column
df_programs = df.dropna(subset=['Program']).copy()

# Step 3: Reshape the month/year columns into a long format
# We're going to melt the dataframe to have one row per Year/Month/Qty
df_melted = df_programs.melt(
    id_vars=['Family', 'Program', 'Status', 'Group Code', 'Data Source'],  # Adjust these as needed
    var_name=['Year', 'Month'],  # Handle the multi-level column headers
    value_name='Quantity'
)

# Step 4: Clean up the 'Month' column if necessary (e.g., J, F, M can be mapped to full names)
month_mapping = {'J': 'January', 'F': 'February', 'M': 'March', 'A': 'April', 'M': 'May', 'J': 'June',
                 'J': 'July', 'A': 'August', 'S': 'September', 'O': 'October', 'N': 'November', 'D': 'December'}
df_melted['Month'] = df_melted['Month'].map(month_mapping)

# Step 5: Output the cleaned dataframe
print(df_melted.head())