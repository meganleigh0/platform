import pandas as pd

def summarize_pipeline(self):
    # Assuming 'Operations' is a list of tuples where the first element is hours and the third is the department
    # First, let's explode the 'Operations' so each operation is a separate row
    df_exploded = self.df_lim.explode('Operations')
    
    # Extract parts, operation hours, and departments from exploded operations
    df_exploded[['Operation Hours', 'Department']] = pd.DataFrame(df_exploded['Operations'].tolist(), index=df_exploded.index)
    
    # Aggregate data for each station
    agg_data = {
        'Parts': lambda x: (x['Operations'].isnull() | x['Operations'].str.len() == 0).sum(),
        'Assemblies': lambda x: x['Operations'].apply(lambda ops: len(ops) > 0).sum(),
        'Operations': 'size',
        'Total Operation Hours': 'sum',
        'Departments': lambda x: x['Department'].dropna().unique()
    }
    
    summary_df = df_exploded.groupby('Station').agg(agg_data)
    
    # Post-processing for correct column names and formats
    summary_df['Operations'] = summary_df['Operations'] - summary_df['Parts']  # Adjust Operations count
    summary_df['Departments'] = summary_df['Departments'].apply(lambda x: ', '.join(sorted(x)))
    
    # Rename columns if necessary
    summary_df.columns = ['Parts', 'Assemblies', 'Operations', 'Total Operation Hours', 'Departments']
    
    self.visualize_summary(summary_df)
