import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Assuming 'final_df' is your dataframe and it's already sorted by 'Timestamp_start'

# Initialize subplots
fig = make_subplots(rows=3, cols=1, subplot_titles=('View by Vehicle', 'View by Station', 'View by Assembly'))

# Add traces for each vehicle
for vehicle in final_df['Vehicle'].unique():
    df_vehicle = final_df[final_df['Vehicle'] == vehicle]
    fig.add_trace(
        go.Scatter(
            x=df_vehicle['Timestamp_start'], 
            y=df_vehicle['Station'],
            mode='lines',
            name=f'Vehicle {vehicle}'
        ), row=1, col=1
    )

# Add traces for each station
for station in final_df['Station'].unique():
    df_station = final_df[final_df['Station'] == station]
    fig.add_trace(
        go.Scatter(
            x=df_station['Timestamp_start'], 
            y=df_station['Vehicle'],
            mode='lines',
            name=f'Station {station}'
        ), row=2, col=1
    )

# Add traces for each assembly
for assembly in final_df['AssemblyID'].unique():
    df_assembly = final_df[final_df['AssemblyID'] == assembly]
    fig.add_trace(
        go.Scatter(
            x=df_assembly['Timestamp_start'], 
            y=df_assembly['Station'],
            mode='lines',
            name=f'Assembly {assembly}'
        ), row=3, col=1
    )

# Update layout for a cleaner look
fig.update_layout(
    height=1200, 
    showlegend=False,
    title_text="Interactions by Vehicle, Station, and Assembly",
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{"visible": [True] * len(final_df['Vehicle'].unique()) + [False] * (len(final_df['Station'].unique()) + len(final_df['AssemblyID'].unique()))}],
                    label="Vehicle",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False] * len(final_df['Vehicle'].unique()) + [True] * len(final_df['Station'].unique()) + [False] * len(final_df['AssemblyID'].unique())}],
                    label="Station",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False] * (len(final_df['Vehicle'].unique()) + len(final_df['Station'].unique())) + [True] * len(final_df['AssemblyID'].unique())}],
                    label="Assembly",
                    method="update"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

# Add dropdown menu with options
fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "label": "By Vehicle",
                    "method": "update",
                    "args": [{"visible": [True if 'Vehicle' in trace.name else False for trace in fig.data]}],
                },
                {
                    "label": "By Station",
                    "method": "update",
                    "args": [{"visible": [True if 'Station' in trace.name else False for trace in fig.data]}],
                },
                {
                    "label": "By Assembly",
                    "method": "update",
                    "args": [{"visible": [True if 'Assembly' in trace.name else False for trace in fig.data]}],
                },
            ],
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.1,
            "xanchor": "left",
            "y": 1.22,
            "yanchor": "top"
        },
    ]
)

fig.show()