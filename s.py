matches = []
for assembly in assembly_list:
    match = fuzzy_match(assembly, df['Description'])
    mbom_id = df.loc[df['Description'] == match[0], 'mbomID'].iloc[0]
    matches.append((assembly, match[0], mbom_id, match[1]))

# Convert the matches to a DataFrame for better visualization
matches_df = pd.DataFrame(matches, columns=['Assembly', 'Matched_Description', 'mbomID', 'Score'])