# Step 1: Merge on 'Operation' from df and 'OperNo' from final_df, as well as 'OpSheet'
merged_df = pd.merge(df, final_df, left_on=['Operation', 'OpSheet'], right_on=['OperNo', 'OpSheet'], how='left')

# Step 2: Handle one-to-many relationship by ensuring all 'StepNo' and other details are captured from final_df
# If needed, group by the 'Operation' and 'OpSheet' in df to capture multiple steps
# For this example, the merge already captures all the necessary parts from final_df

# Step 3: (Optional) Fill any unmatched values or track unmatched rows if necessary
unmatched_rows = merged_df[merged_df['PartAction'].isna()]

# Step 4: Display the merged result and any unmatched rows
print("Merged DataFrame:\n", merged_df)
print("\nUnmatched rows:\n", unmatched_rows)