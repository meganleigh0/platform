# If duplicates are found, rename them by appending unique suffixes
df.columns = pd.Index([f"{col[0]}_{i}" if col in duplicate_columns else col for i, col in enumerate(df.columns)])

# Print the new column names to confirm
print(df.columns)