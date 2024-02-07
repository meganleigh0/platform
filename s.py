# Step 1: Identify contiguous blocks of the same PlanNo
df['block'] = (df['PlanNo'] != df['PlanNo'].shift()).cumsum()

# Step 2: For PlanNos appearing in more than one block, keep only the rows from the last block
# This involves finding the last block for each PlanNo and then filtering the DataFrame based on these blocks
last_blocks = df.groupby('PlanNo')['block'].max().reset_index()

# Filter the original DataFrame to keep rows that are in the last block for their respective PlanNo
filtered_df_corrected = df[df.apply(lambda x: x['block'] in last_blocks.loc[last_blocks['PlanNo'] == x['PlanNo'], 'block'].values, axis=1)]

# Drop the auxiliary 'block' column used for identifying contiguous blocks
filtered_df_corrected = filtered_df_corrected.drop(columns=['block'])

filtered_df_corrected
