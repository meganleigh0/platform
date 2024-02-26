# Function to match criticality based on station and description
def match_criticality(df_lim, critcal_parts):
    # Map for criticality based on station
    station_criticality = critcal_parts.set_index('Station')['Criticality'].to_dict()
    
    # Initially, try to match based on Station
    df_lim['Criticality'] = df_lim['Station'].map(station_criticality)
    
    # For unmatched items, attempt to find best match based on description
    unmatched = df_lim[df_lim['Criticality'].isna()]
    
    if not unmatched.empty:
        for index, row in unmatched.iterrows():
            # Find best matching assembly description using a fuzzy matching library
            best_match, score = process.extractOne(row['Description'], critcal_parts['Assembly'].tolist())
            
            # If the match score is above a certain threshold, assign criticality
            if score > 80:  # Threshold can be adjusted based on accuracy needs
                matched_criticality = critcal_parts[critcal_parts['Assembly'] == best_match]['Criticality'].values[0]
                df_lim.at[index, 'Criticality'] = matched_criticality

    return df_lim

# Applying the matching function
df_lim_updated = match_criticality(df_lim, critcal_parts)
df_lim_updated
