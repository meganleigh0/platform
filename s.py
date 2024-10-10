# Step 1: Merge based on 'OpSheet' and 'OpNum' from df to 'OpSheet' and 'OperNo' from final_df
merged_df = pd.merge(df, final_df, left_on=['OpSheet', 'OpNum'], right_on=['OpSheet', 'OperNo'], how='left')

# Step 2: Verify if there are any unmatched rows (Optional)
unmatched_rows = merged_df[merged_df['OperNo'].isna()]

# Step 3: Display the final merged DataFrame and any unmatched rows
print("Merged DataFrame:\n", merged_df)
print("\nUnmatched rows:\n", unmatched_rows)