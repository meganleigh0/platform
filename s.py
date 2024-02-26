import matplotlib.pyplot as plt
import pandas as pd

def summarize_pipeline(self):
    unique_departments = set()
    summary_data = {}
    
    for index, row in self.df_lim.iterrows():
        # Update unique departments from operations
        for operation in row['Operations']:
            if operation:  # Checks if the operation is not an empty list
                unique_departments.add(operation[2])  # department is the 3rd item
        
        station = row['Station']
        # Initialize station data in summary
        if station not in summary_data:
            summary_data[station] = {'Parts': 0, 'Assemblies': 0, 'Operations': 0}
        
        # Count parts and assemblies
        if row['Operations']:
            summary_data[station]['Assemblies'] += 1
        else:
            summary_data[station]['Parts'] += 1
        
        # Count operations
        summary_data[station]['Operations'] += len(row['Operations'])
    
    # Convert summary data to DataFrame for reporting and visualization
    summary_df = pd.DataFrame.from_dict(summary_data, orient='index', columns=['Parts', 'Assemblies', 'Operations'])
    
    # Print the formatted table
    print("\nMBOM Pipeline Summary Table\n")
    print(summary_df)
    
    # Optionally, include a visual summary
    self.visualize_summary(summary_df)

def visualize_summary(self, summary_df):
    # Plotting summary as a stacked bar chart
    summary_df.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Parts, Assemblies, and Operations by Station')
    plt.xlabel('Station')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Type')
    plt.tight_layout()
    plt.show()
