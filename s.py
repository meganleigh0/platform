def match_criticality(df_lim, critcal_parts):
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    # Fit on the combined set of text for better vectorization
    vectorizer.fit(pd.concat([df_lim['Description'], critcal_parts['Assembly']]))

    # Vectorize descriptions and assemblies
    desc_vectors = vectorizer.transform(df_lim['Description'])
    assembly_vectors = vectorizer.transform(critcal_parts['Assembly'])

    # Compute cosine similarity
    similarity = cosine_similarity(desc_vectors, assembly_vectors)

    # For each item in df_lim, find the best match in critcal_parts based on similarity
    best_matches = similarity.argmax(axis=1)
    df_lim['Criticality'] = critcal_parts.iloc[best_matches]['Criticality'].values
    df_lim['Matched Assembly'] = critcal_parts.iloc[best_matches]['Assembly'].values

    return df_lim

# Apply the function
df_lim_updated = match_criticality(df_lim, critcal_parts)
