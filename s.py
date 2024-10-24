import pandas as pd

# Load the Excel file with multi-level header
file_path = "path_to_your_excel_file.xlsx"
df = pd.read_excel(file_path, header=[0, 1])  # Multi-level header for Year/Month

# Step 1: Identify the rows where Status and other columns have zero or blank (indicating a Family row)
# Assuming columns like 'Status', 'Group Code', etc. are used for families and filled with '0' for families
df['Is_Family'] = df['Status'].apply(lambda x: x == 0) & df['Group Code'].apply(lambda x: x == 0)

# Step 2: Fill down the Family values into a new 'Family' column
df['Family'] = df.loc[df['Is_Family'], df.columns[0]]  # Capture the first column (family names)
df['Family'].ffill(inplace=True)  # Fill down the Family names

# Step 3: Remove the Family rows themselves since they've been captured and propagated
df_filtered = df[~df['Is_Family']].copy()

# Step 4: Separate Programs from Families in the same column (Program column will be same as Family column)
df_filtered['Program'] = df_filtered[df_filtered.columns[0]]  # Assuming column 0 contains Program names

# Step 5: Reshape the month/year columns into a long format
df_melted = df_filtered.melt(
    id_vars=['Family', 'Program', 'Status', 'Group Code', 'Data Source'],  # Adjust based on your columns
    var_name=['Year', 'Month'],  # Use the multi-level header
    value_name='Quantity'
)

# Step 6: Output the cleaned dataframe
print(df_melted.head())