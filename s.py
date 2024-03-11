# Adjusting the DataFrame to concatenate mbomID with the variant name for uniqueness
def adjust_df(df, variant_name):
    # This function assumes 'mbomID' is part of the index
    # If it's not, you might need to set it first using df.set_index([...], inplace=True)
    df.index = df.index.set_levels(df.index.levels[-3].astype(str) + '_' + variant_name, level=-3) # Adjusting the level for 'mbomID' assuming it's the third level in the index
    return df

# Apply the adjustment to each DataFrame before concatenating
adjusted_dfs = {variant: adjust_df(df.copy(), variant) for variant, df in longest_operations.items()}

# Now concatenate all adjusted DataFrames into one
all_operations_df = pd.concat(adjusted_dfs.values(), keys=adjusted_dfs.keys(), names=['Variant', 'Index'])

# Proceed with the analysis as before