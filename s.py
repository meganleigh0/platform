import pandas as pd

# Load the dataframe (assuming it's already loaded in your case)
# df = pd.read_excel('your_file.xlsx')  # Uncomment this if you're loading from an Excel file

# Step 1: Remove initial blank rows
df_clean = df.dropna(how='all').reset_index(drop=True)

# Step 2: Set the correct header row
# Assuming row 0 has the program/family, and row 1 has year information with months below it
new_columns = df_clean.iloc[1].fillna('') + '_' + df_clean.iloc[2].fillna('')
new_columns = new_columns.str.strip('_')  # Clean up any extra underscores from empty cells

# Step 3: Assign the new column names and drop the old header rows
df_clean.columns = new_columns
df_clean = df_clean.drop([0, 1, 2])

# Step 4: Clean up remaining blank columns or unnecessary columns if needed
df_clean = df_clean.dropna(axis=1, how='all')  # Drop any fully blank columns
df_clean = df_clean.reset_index(drop=True)

# Step 5: (Optional) Clean up and format remaining data as needed
# For example, you may want to split the program/family information into separate columns

# Display the cleaned dataframe
df_clean.head()