# Separate start and end interactions
start_df = df[df['Interaction'] == 'start']
end_df = df[df['Interaction'] == 'end']

# Merge on AssemblyID, Station, and Vehicle
merged_df = pd.merge(start_df, end_df, on=['AssemblyID', 'Station', 'Vehicle'], suffixes=('_start', '_end'))

# Extract necessary columns
final_df = merged_df[['AssemblyID', 'Station', 'Timestamp_start', 'Timestamp_end', 'Vehicle']]
import plotly.graph_objects as go

fig = go.Figure()

# Add a trace for each vehicle
for vehicle in final_df['Vehicle'].unique():
    vehicle_df = final_df[final_df['Vehicle'] == vehicle]
    for _, row in vehicle_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Timestamp_start'], row['Timestamp_end']],
            y=[row['Station'], row['Station']],
            mode='lines',
            name=f'Vehicle {vehicle}',
            line=dict(width=10)
        ))

fig.update_layout(
    title='Assembly Interactions by Vehicle and Station',
    xaxis_title='Timestamp',
    yaxis_title='Station',
    yaxis_categoryorder='total descending'
)

fig.show()
