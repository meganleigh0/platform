import plotly.graph_objects as go

# Assuming final_df is your dataframe with the columns: 'AssemblyID', 'Station', 'Vehicle', 'Timestamp_start', and 'Timestamp_end'

# Create the figure
fig = go.Figure()

# Get unique identifiers for dropdown options
stations = final_df['Station'].unique()
vehicles = final_df['Vehicle'].unique()
assemblies = final_df['AssemblyID'].unique()

# Add all bars initially
for i, row in final_df.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[row['Timestamp_start'], row['Timestamp_end']],
            y=[row['Station'], row['Station']],
            mode='lines',
            name=f'Vehicle {row["Vehicle"]}',
            line=dict(color=f'rgba({row["Vehicle"]*12}, {100 + row["Vehicle"]*5}, {150 + row["Vehicle"]*5}, 0.8)'),
            legendgroup=f'Vehicle {row["Vehicle"]}',
            showlegend=i==0, # show legend only for the first line of each vehicle
            hoverinfo='text',
            text=f'Vehicle: {row["Vehicle"]}<br>AssemblyID: {row["AssemblyID"]}<br>Time Start: {row["Timestamp_start"]}<br>Time End: {row["Timestamp_end"]}'
        )
    )

# Update the layout to include dropdown menus
fig.update_layout(
    updatemenus=[
        {'buttons': [
            {
                'method': 'update',
                'label': 'All Stations',
                'args': [{'visible': [True] * len(final_df)}, {'title': 'All Stations'}]
            },
            *[
                {
                    'method': 'update',
                    'label': f'Station {station}',
                    'args': [{'visible': [True if station == row['Station'] else False for _, row in final_df.iterrows()]},
                             {'title': f'Station {station}'}]
                } for station in stations
            ],
            {
                'method': 'update',
                'label': 'All Vehicles',
                'args': [{'visible': [True] * len(final_df)}, {'title': 'All Vehicles'}]
            },
            *[
                {
                    'method': 'update',
                    'label': f'Vehicle {vehicle}',
                    'args': [{'visible': [True if vehicle == row['Vehicle'] else False for _, row in final_df.iterrows()]},
                             {'title': f'Vehicle {vehicle}'}]
                } for vehicle in vehicles
            ],
            {
                'method': 'update',
                'label': 'All Assemblies',
                'args': [{'visible': [True] * len(final_df)}, {'title': 'All Assemblies'}]
            },
            *[
                {
                    'method': 'update',
                    'label': f'Assembly {assembly}',
                    'args': [{'visible': [True if assembly == row['AssemblyID'] else False for _, row in final_df.iterrows()]},
                             {'title': f'Assembly {assembly}'}]
                } for assembly in assemblies
            ],
        ],
         'direction': 'down',
         'showactive': True,
        }
    ],
    title="Assembly Interactions by Vehicle and Station"
)

# Set y-axis to have the stations in the desired order
fig.update_yaxes(type='category')

# Show the figure
fig.show()