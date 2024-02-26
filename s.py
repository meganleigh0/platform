import pandas as pd
import plotly.graph_objects as go

def summarize_pipeline(self):
    unique_departments = set()
    summary_data = {}
    
    for index, row in self.df_lim.iterrows():
        station = row['Station']
        # Initialize station data in summary if not already present
        if station not in summary_data:
            summary_data[station] = {'Parts': 0, 'Assemblies': 0, 'Operations': 0, 'Total Operation Hours': 0, 'Departments': set()}
        
        # Update unique departments and count parts, assemblies, and sum operation hours
        for operation in row['Operations']:
            summary_data[station]['Departments'].add(operation[2])  # Add department to set
        
        if row['Operations']:
            summary_data[station]['Assemblies'] += 1
            summary_data[station]['Total Operation Hours'] += sum(op[0] for op in row['Operations'])
        else:
            summary_data[station]['Parts'] += 1
        
        summary_data[station]['Operations'] += len(row['Operations'])
    
    # Prepare DataFrame
    for station in summary_data:
        summary_data[station]['Departments'] = ', '.join(sorted(summary_data[station]['Departments']))  # Convert set to sorted comma-separated string
    summary_df = pd.DataFrame.from_dict(summary_data, orient='index', columns=['Parts', 'Assemblies', 'Operations', 'Total Operation Hours', 'Departments'])
    
    self.visualize_summary(summary_df)

def visualize_summary(self, summary_df):
    # Creating the plot with Plotly
    fig = go.Figure(data=[
        go.Bar(name='Parts', x=summary_df.index, y=summary_df['Parts'], marker_color='blue'),
        go.Bar(name='Assemblies', x=summary_df.index, y=summary_df['Assemblies'], marker_color='green'),
        go.Bar(name='Operations', x=summary_df.index, y=summary_df['Operations'], marker_color='orange'),
        go.Scatter(name='Total Operation Hours', x=summary_df.index, y=summary_df['Total Operation Hours'], mode='lines+markers', yaxis='y2', line=dict(color='red')),
    ])
    
    # Adding departments as hover information
    hover_texts = ['Departments: ' + dept for dept in summary_df['Departments']]
    fig.update_traces(hoverinfo='text', text=hover_texts)
    
    # Customize layout
    fig.update_layout(
        barmode='group',
        title='Summary by Station: Parts, Assemblies, Operations, and Total Operation Hours',
        xaxis_tickangle=-45,
        xaxis_title='Station',
        yaxis=dict(title='Count', side='left'),
        yaxis2=dict(title='Total Operation Hours', overlaying='y', side='right'),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig.show()
