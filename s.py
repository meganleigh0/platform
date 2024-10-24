import pandas as pd

import pandas as pd


# Rename columns for ease of access
df.columns = [f"Unnamed_{i}" if col.startswith("Unnamed") else col for i, col in enumerate(df.columns)]

# Identify the "Program" column and the Year/Quarter columns
program_col = 'Program'
year_quarter_columns = df.columns[3:]  # Assuming the first 3 columns are for sectioning and program

# Melt the dataframe to make it easier to handle (reshape it)
df_melted = pd.melt(df, id_vars=[program_col], value_vars=year_quarter_columns, var_name='Year_Quarter', value_name='Quantity')

# Split the 'Year_Quarter' into separate 'Year' and 'Quarter' columns
df_melted[['Year', 'Quarter']] = df_melted['Year_Quarter'].str.extract(r'(\d+)(Q\d)')

# Convert the Year and Quarter columns to appropriate datatypes
df_melted['Year'] = df_melted['Year'].astype(int)
df_melted['Quantity'] = df_melted['Quantity'].astype(float)

# Fill in missing quarters/months by distributing the quantity evenly if not broken down
def distribute_quantity(row):
    if row['Quantity'] != 0 and row['Quarter']:
        return row['Quantity'] / 3  # Divide into three months for simplicity
    return row['Quantity']

df_melted['Distributed_Quantity'] = df_melted.apply(distribute_quantity, axis=1)

# View the result
df_melted.head()