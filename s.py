stations = df['Station'].unique()
stations.sort()

# Create a list for the dropdown options
dropdown_options = [{'label': 'All Stations', 'method': 'update', 'args': [{'visible': [True] * len(df)}]}]
for station in stations:
    # Boolean list to set 'visible' property
    visibility = [row['Station'] == station for index, row in df.iterrows()]
    dropdown_option = {
        'label': station,
        'method': 'update',
        'args': [{'visible': visibility}]
    }
    dropdown_options.append(dropdown_option)

# Create traces for the Gantt chart
traces = []
for index, row in df.iterrows():
    traces.append(
        go.Bar(
            x=[row['Timestamp_end'] - row['Timestamp_start']],
            y=['{} - {}'.format(row['Assembly'], row['Station'])],
            base=row['Timestamp_start'],
            name=row['Vehicle'],
            orientation='h',
            marker=dict(color=hash(row['Vehicle']) & 0xFFFFFF),  # Color by vehicle
        )
    )

# Create the figure with the traces
fig = go.Figure(data=traces)

# Add dropdown
fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_options,
        'direction': 'down',
        'showactive': True,
    }],
    title="Gantt Chart by Station and Vehicle",
    xaxis_title="Time",
    yaxis_title="Assembly - Station",
    barmode='stack'
)

# Show the figure
fig.show()
