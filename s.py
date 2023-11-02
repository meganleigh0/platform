fig = go.Figure()

# Reduce the width of the lines and add opacity
line_width = 4
line_opacity = 0.7

# Add a trace for each vehicle
for vehicle, color in color_dict.items():
    vehicle_df = final_df[final_df['Vehicle'] == vehicle].sort_values(by=['Timestamp_start'])

    x_values = []
    y_values = []
    hover_text = []
    for _, row in vehicle_df.iterrows():
        # Apply jitter to the y-axis values
        jitter = np.random.uniform(-0.3, 0.3)  # Adjust the range as needed
        station_with_jitter = f"{row['Station']} {jitter}"
        
        x_values.extend([row['Timestamp_start'], row['Timestamp_end'], None])
        y_values.extend([station_with_jitter, station_with_jitter, None])
        hover_info = f"AssemblyID: {row['AssemblyID']}<br>Vehicle: {vehicle}"
        hover_text.extend([hover_info, hover_info, None])

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name=f'Vehicle {vehicle}',
        line=dict(width=line_width, color=color, opacity=line_opacity),
        hoverinfo='text',
        text=hover_text
    ))

# Update the layout to use the jittered station names if necessary
fig.update_layout(
    title='Assembly Interactions by Vehicle and Station',
    xaxis_title='Timestamp',
    yaxis_title='Station',
    yaxis=dict(
        categoryorder='array',
        categoryarray=[f"{station} {jitter_val}" for station in station_order for jitter_val in np.linspace(-0.3, 0.3, 3)]  # Update this as per your jitter logic
    )
)

fig.show()