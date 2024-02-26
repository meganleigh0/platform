import matplotlib.pyplot as plt
import pandas as pd

def summarize_pipeline(self):
    unique_departments = set()
    operations_by_station = {}
    parts_and_assemblies_by_station = {}
    
    for index, row in self.df_lim.iterrows():
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
            
    # Print formatted output
    print("MBOM Pipeline Summary\n")
    print(f"Unique Departments: {sorted(list(unique_departments))}")
    print("\nOperations by Station:")
    for station, count in operations_by_station.items():
        print(f"  {station}: {count} operations")
    print("\nParts and Assemblies by Station:")
    for station, counts in parts_and_assemblies_by_station.items():
        print(f"  {station}: {counts['Parts']} parts, {counts['Assemblies']} assemblies")
    
    # Optionally, include a visual summary
    self.visualize_summary(operations_by_station, parts_and_assemblies_by_station)

def visualize_summary(self, operations_by_station, parts_and_assemblies_by_station):
    # Convert dictionaries to DataFrames for plotting
    ops_df = pd.DataFrame(list(operations_by_station.items()), columns=['Station', 'Operations'])
    parts_assemblies_df = pd.DataFrame(parts_and_assemblies_by_station).T.reset_index()
    parts_assemblies_df.columns = ['Station', 'Parts', 'Assemblies']
    
    # Plotting operations by station
    plt.figure(figsize=(10, 6))
    plt.bar(ops_df['Station'], ops_df['Operations'], color='skyblue')
    plt.title('Operations Count by Station')
    plt.xlabel('Station')
    plt.ylabel('Operations Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plotting parts and assemblies by station
    parts_assemblies_df.plot(x='Station', kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Parts and Assemblies Count by Station')
    plt.xlabel('Station')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
