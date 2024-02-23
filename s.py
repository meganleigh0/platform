 for name, variations in station_names.items():
        pattern = '|'.join(variations)
        df['Station'] = df['Station'].str.replace(pattern, name, case=False, regex=True)
    
    # Divorce assignment
