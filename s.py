def summarize_pipeline(df_lim):
    unique_departments = set()
    operations_by_station = {}
    parts_and_assemblies_by_station = {}
    
    for index, row in df_lim.iterrows():
        # Update unique departments
        for operation in row['Operations']:
            if operation:  # Checks if the operation is not an empty list
                unique_departments.add(operation[2])  # department is the 3rd item
                
        # Initialize or update operations count by station
        station = row['Station']
        operations_by_station[station] = operations_by_station.get(station, 0) + len(row['Operations'])
        
        # Initialize parts and assemblies count for the station
        if station not in parts_and_assemblies_by_station:
            parts_and_assemblies_by_station[station] = {'Parts': 0, 'Assemblies': 0}
        
        # Update parts and assemblies count
        if row['Operations']:
            parts_and_assemblies_by_station[station]['Assemblies'] += 1
        else:
            parts_and_assemblies_by_station[station]['Parts'] += 1
            
    return {
        'Unique Departments': unique_departments,
        'Operations by Station': operations_by_station,
        'Parts and Assemblies by Station': parts_and_assemblies_by_station
    }

# Example usage
# summary = summarize_pipeline(df_lim)
# print(summary)
