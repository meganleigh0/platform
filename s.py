import pandas as pd

# Step 1: Load the Excel file with multi-level header
file_path = "path_to_your_excel_file.xlsx"  # Adjust path
df = pd.read_excel(file_path, header=[0, 1])  # Multi-level header for Year/Month

# Step 2: Check for duplicate columns
duplicate_columns = df.columns[df.columns.duplicated()]
if not duplicate_columns.empty:
    # Rename duplicate columns by appending a suffix
    df.columns = pd.Index([f"{col[0]}_{i}" if col in duplicate_columns else col for i, col in enumerate(df.columns)])

# Step 3: Identify Family rows by checking for zeros in 'Status' and 'Group Code' columns
df['Is_Family'] = (df[('Unnamed: 0_level_0', 'Status')] == 0) & (df[('Unnamed: 1_level_0', 'Group Code')] == 0)

# Step 4: Fill down the Family values into a new 'Family' column
df['Family'] = df.loc[df['Is_Family'], df.columns[0]]  # Capture the first column (family names)
df['Family'].ffill(inplace=True)  # Fill down the Family names

# Step 5: Remove the Family rows themselves since they’ve been captured and propagated
df_filtered = df[~df['Is_Family']].copy()

# Step 6: Separate Programs from Families in the same column (Program column will be same as Family column)
df_filtered['Program'] = df_filtered[df_filtered.columns[0]]  # Assuming column 0 contains Program names

# Step 7: Reshape the month/year columns into a long format
df_melted = df_filtered.melt(
    id_vars=['Family', 'Program', ('Unnamed: 0_level_0', 'Status'), ('Unnamed: 1_level_0', 'Group Code')], 
    var_name=['Year', 'Month'],  # Adjust based on your actual columns
    value_name='Quantity'
)

# Step 8: Output the cleaned dataframe
print(df_melted.head())