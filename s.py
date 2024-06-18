import plotly.graph_objects as go
import pandas as pd

# Assuming df is your DataFrame

# Convert 'Source' to datetime to sort it correctly in the plot
df['Source'] = pd.to_datetime(df['Source'], format='%B_%Y')

# Sort the DataFrame by Source to ensure chronological plotting
df.sort_values('Source', inplace=True)

# Create a figure with a dropdown menu to select plants
fig = go.Figure()

# Get unique plant names
plants = df['Plant'].unique()

# Loop over each plant to create a plot for each
for plant in plants:
    filtered_df = df[df['Plant'] == plant]

    for dept in filtered_df['DEPT'].unique():
        fig.add_trace(
            go.Bar(
                x=filtered_df[filtered_df['DEPT'] == dept]['Source'],
                y=filtered_df[filtered_df['DEPT'] == dept]['EstimatedHours'],
                name=str(dept),
                visible=(plant == plants[0])  # Only the first plant is visible initially
            )
        )

# Create dropdown menus
buttons = [
    dict(
        label=plant,
        method='update',
        args=[{'visible': [plant == k for k in plants for _ in df[df['Plant'] == k]['DEPT'].unique()]}]
        # Nested comprehension to manage visibility per plant and department
    ) for plant in plants
]

fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.0,
        xanchor='left',
        y=1.1,
        yanchor='top'
    )],
    title='Estimated Hours by Department and Source',
    xaxis_title='Report Month',
    yaxis_title='Estimated Hours',
    barmode='stack',
    xaxis=dict(
        tickformat='%b %Y',  # Format the ticks to show abbreviated month and year
        tickangle=-45
    )
)

fig.show()