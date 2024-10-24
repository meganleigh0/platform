# Step 2: Fill down the Family values into a new 'Family' column
df['Family'] = df.loc[df['Is_Family'], df.columns[0]]  # Capture the first column (family names)
df['Family'].ffill(inplace=True)  # Fill down the Family names

# Step 3: Remove the Family rows themselves since they’ve been captured and propagated
df_filtered = df[~df['Is_Family']].copy()

# Step 4: Separate Programs from Families in the same column (Program column will be same as Family column)
df_filtered['Program'] = df_filtered[df_filtered.columns[0]]  # Assuming column 0 contains Program names

# Step 5: Reshape the month/year columns into a long format
df_melted = df_filtered.melt(
    id_vars=['Family', 'Program', ('Unnamed: 0_level_0', 'Status'), ('Unnamed: 1_level_0', 'Group Code')], 
    var_name=['Year', 'Month'],  # Adjust based on your actual columns
    value_name='Quantity'
)

# Step 6: Output the cleaned dataframe
print(df_melted.head())