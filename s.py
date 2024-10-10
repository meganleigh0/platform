})

# Step 1: First, merge on the 'opnum' (df1) and 'opernum' (df2)
merged_df = pd.merge(df1, df2, left_on='opnum', right_on='opernum', how='left', suffixes=('_df1', '_df2'))

# Step 2: For rows where there are duplicates (non-unique 'opnum'), re-merge on both 'opnum' and 'opsheet'
# Merge on both 'opnum' and 'opsheet' for more specific matching (handling duplicates)
df_with_match = pd.merge(df1, df2, left_on=['opnum', 'opsheet'], right_on=['opernum', 'opsheet'], how='left', suffixes=('_df1', '_df2'))

# Step 3: Fill missing values in the initial merge (from opnum matching) with the more specific match (opnum + opsheet)
merged_df.update(df_with_match)

# Step 4: For any unmatched rows, fill missing 'value2' or the merged column with 0 or your preferred default value
merged_df['value2'].fillna(0, inplace=True)

# Now merged_df contains both direct and conditional merges based on your criteria
print(merged_df)