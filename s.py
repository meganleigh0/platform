import pandas as pd

# Example DataFrames
df1 = pd.DataFrame({
    'opnum': [101, 102, 103, 104, 105],
    'opsheet': [1, 1, 2, 2, 3],
    'value1': [10, 20, 30, 40, 50]
})

df2 = pd.DataFrame({
    'opernum': [101, 102, 102, 104, 105],
    'opsheet': [1, 1, 2, 2, 3],
    'value2': [100, 200, 300, 400, 500]
})

# Step 1: Merge first on both 'opnum' and 'opsheet'
merged_df = pd.merge(df1, df2, left_on=['opnum', 'opsheet'], right_on=['opernum', 'opsheet'], how='left', suffixes=('_df1', '_df2'))

# Step 2: Identify rows where no match was found in step 1 (null 'value2')
unmatched_df = merged_df[merged_df['value2'].isna()]

# Step 3: For those unmatched rows, re-merge based only on 'opnum'
if not unmatched_df.empty:
    fallback_df = pd.merge(df1, df2[['opernum', 'value2']], left_on='opnum', right_on='opernum', how='left')
    
    # Update the original merged_df with the fallback matches where 'value2' was missing
    merged_df.update(fallback_df[['opnum', 'value2']])

# Step 4: Fill any remaining missing values in 'value2' with a default (e.g., 0)
merged_df['value2'].fillna(0, inplace=True)

# Now merged_df contains both direct and fallback merges
print(merged_df)