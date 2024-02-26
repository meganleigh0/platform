def map_criticality(df_lim, critcal_parts):
    # Initialize a column for criticality in df_lim
    df_lim['Criticality'] = np.nan

    # Direct Station Code Matching
    station_mapping = dict(zip(critcal_parts['Normalized Station'], critcal_parts['Criticality']))
    for index, row in df_lim.iterrows():
        if row['Normalized Station'] in station_mapping:
            df_lim.at[index, 'Criticality'] = station_mapping[row['Normalized Station']]

    # Fuzzy Matching for Descriptions where Criticality is NaN
    vectorizer = TfidfVectorizer()
    assembly_desc_vectors = vectorizer.fit_transform(critcal_parts['Normalized Assembly'])
    
    for index, row in df_lim[df_lim['Criticality'].isna()].iterrows():
        description_vector = vectorizer.transform([row['Normalized Description']])
        similarity_scores = cosine_similarity(description_vector, assembly_desc_vectors)
        
        # Find the best match with a similarity score threshold, e.g., 0.5
        best_match_index = similarity_scores.argmax()
        best_match_score = similarity_scores[0, best_match_index]
        
        if best_match_score > 0.5:  # Threshold for a clear match
            df_lim.at[index, 'Criticality'] = critcal_parts.iloc[best_match_index]['Criticality']

    return df_lim.drop(columns=['Normalized Station', 'Normalized Description'])

# Apply the function
df_lim_updated = map_criticality(df_lim, critcal_parts)
df_lim_updated
