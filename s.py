import plotly.graph_objects as go

def visualize_connections(df):
    fig = go.Figure()

    assemblies = df['AssemblyID'].unique()
    for assembly in assemblies:
        subset_df = df[df['AssemblyID'] == assembly]
        start_row = subset_df[subset_df['Interaction'] == 'Start']
        complete_row = subset_df[subset_df['Interaction'] == 'Complete']

        if not start_row.empty and not complete_row.empty:
            fig.add_trace(go.Scatter(
                x=[start_row['Timestamp'].values[0], complete_row['Timestamp'].values[0]],
                y=[start_row['AssemblyID'].values[0], complete_row['AssemblyID'].values[0]],
                mode='lines+markers',
                name=f"Assembly {assembly}"
            ))

    fig.update_layout(title="Connections between Start and Complete of Assemblies",
                      xaxis_title="Timestamp",
                      yaxis_title="AssemblyID")

    fig.show()

# Sample data
df = pd.DataFrame({
    'Timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'Interaction': ['Start', 'Complete', 'Start', 'Complete'],
    'AssemblyID': [1, 1, 2, 2]
})

visualize_connections(df)