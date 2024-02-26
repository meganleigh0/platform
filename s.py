df_lim['Normalized Description'] = df_lim['Description'].apply(lambda x: preprocess_text(x))
critcal_parts['Normalized Assembly'] = critcal_parts['Assembly'].apply(lambda x: preprocess_text(x))
