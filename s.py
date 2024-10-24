import pandas as pd

# Load the Excel file


# Rename the "Unnamed" columns properly if possible
df.columns = [col if not col.startswith("Unnamed") else f"Unnamed_{i}" for i, col in enumerate(df.columns)]

# Assuming 'Program' is correctly loaded, you can filter the columns for the ones representing months/quarters
# Example: filter all columns that represent quantities for Q1, Q2, etc.
quantity_columns = [col for col in df.columns if 'Q' in str(col) or '2015' in str(col)]

# Displaying the Program and its corresponding quantities
df_program_quantities = df[['Program'] + quantity_columns]

# View the first few rows to ensure it's correct
df_program_quantities.head()