def assign_station(df):
    # Initial assignment
    df['Station'] = 'p1'
    
    # Vehicle section assignments
    veh_mask = df['Description'].str.contains('prep|test', case=False)
    df.loc[veh_mask, 'Station'] = df['Description']

    assign_children_for_mask(veh_mask, df)

    # Process final assemblies
    final_assy_mask = df['Description'].str.contains('final')
    df.loc[final_assy_mask, 'Station'] = df['Description'][final_assy_mask].apply(process_final_assembly)

    assign_children_for_mask(final_assy_mask, df)

    df.loc[final_assy_mask, 'Station'] = df['Description'][final_assy_mask].apply(process_final_assembly)

    # Process platforms
    platform_mask = df['Description'].str.contains('platform', case=False)
    df.loc[platform_mask, 'Station'] = 'Platform'

    # Dictionary mappings
    station_names = {
        'Station 1': ['final assy 1', 'final assembly 1', 'final assembly station 1'],
        'Station 2': ['final assy 2', 'final assembly 1'],
        'Station 3': ['final assy 3', 'final assembly 3', 'final assembly station 3'],
    }

    for name, variations in station_names.items():
        for variation in variations:
            df['Station'] = df['Station'].str.replace(variation, name, regex=False)

    # Turret and hull assignments
    for item, station in [('t', 'pa'), ('l', 'pl')]:
        ids = df[df['Description'].str.contains(item)]['mbomID'].tolist()
        df.loc[df['mbomID'].isin(ids), 'Station'] = station
        
        assign_children_by_ids(ids, df, station)

    return df

def assign_children_for_mask(mask, df):
    ids = df[mask]['mbomID'].tolist()
    assign_children_by_ids(ids, df, df.loc[mask, 'Station'])

def assign_children_by_ids(ids, df, station):
    while ids:
        children_ids = df[df['ParentID'].isin(ids)]['mbomID'].tolist()
        df.loc[df['mbomID'].isin(children_ids), 'Station'] = station
        ids = children_ids

def process_final_assembly(desc):
    station_mapping = {
        '12': '1',
        '23': '2',
        '34': '3',
        '45': '4',
        '56': '5',
        '67': '6',
        '78': '7',
        '910': '9',
        '1112': '11'
    }
    
    pattern = r'\b(' + '|'.join(sorted(map(str, station_mapping.keys()), key=len, reverse=True)) + r')\b'    
    return re.sub(pattern, lambda m: station_mapping[m.group(1)], desc)
