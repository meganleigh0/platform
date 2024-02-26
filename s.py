    # Function to apply on each assembly to find the best match
    def find_best_match(assembly):
        # Use fuzzywuzzy to find the best match for the assembly in the descriptions
        best_match = process.extractOne(assembly, descriptions)
        return best_match[0] if best_match else None

    # Apply the function to the Assembly column and create a new column with the results
    assembly_df['Best Match Description'] = assembly_df['Assembly'].apply(find_best_match)
    return assembly_df

# Apply the function
df_matched = match_descriptions(df_assembly, df_description)

print(df_matched)