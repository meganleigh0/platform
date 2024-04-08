import pandas as pd

# Assuming dep_df and exp_df are already defined

# Step 1: Strip whitespace from column names in exp_df
exp_df.columns = exp_df.columns.str.replace(' ', '')

# Rename columns for clarity and consistency
exp_df.rename(columns={'DirectEmployees': 'DirectHeads'}, inplace=True)

# Step 2: Merge dep_df with exp_df to align the DirectHeads
# Merge on dep_df['DepID'] and exp_df['Department'] after stripping any potential whitespace
dep_df['DepID'] = dep_df['DepID'].str.strip()
exp_df['Department'] = exp_df['Department'].str.strip()

# Merging the dataframes to update DirectHeads in dep_df
updated_df = pd.merge(dep_df, exp_df[['Department', 'DirectHeads']], left_on='DepID', right_on='Department', how='left')

# Step 3: Update DirectHeads in dep_df from exp_df
dep_df['DirectHeads'] = updated_df['DirectHeads']

# Now dep_df should have the updated DirectHeads values