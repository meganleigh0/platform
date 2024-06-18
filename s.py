import pandas as pd
import plotly.graph_objects as go

# Example DataFrame
data = {
    'Program': ['Program1', 'Program1', 'Program2', 'Program2'],
    'Family': ['Family1', 'Family1', 'Family2', 'Family2'],
    'Status': ['Active', 'Inactive', 'Active', 'Inactive'],
    'Month': [1, 1, 1, 1],
    'Year': [2020, 2020, 2020, 2020],
    'Vehicles': [100, 150, 200, 250]
}

df = pd.DataFrame(data)

# Aggregate data
df_aggregated = df.groupby(['Family', 'Year', 'Month', 'Program']).agg({'Vehicles': 'sum'}).reset_index()

# Initialize the figure
fig = go.Figure()

# Get unique families
families = df_aggregated['Family'].unique()

# Add traces for each program within each family
for family in families:
    filtered_df = df_aggregated[df_aggregated['Family'] == family]
    for program in filtered_df['Program'].unique():
        fig.add_trace(
            go.Bar(
                x=filtered_df['Month'],
                y=filtered_df[filtered_df['Program'] == program]['Vehicles'],
                name=f'{program} - {family}',
                visible=(family == families[0])  # Only the first family is visible initially
            )
        )

# Create a dropdown menu to select the family
buttons = []

for family in families:
    buttons.append(
        dict(
            label=family,
            method="update",
            args=[{"visible": [family == val.split(' - ')[1] for val in fig.data]},
                  {"title": f"Total Vehicles by Program: {family}"}]
        )
    )

# Add dropdown to the layout
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ],
    title="Total Vehicles by Family and Program",
    xaxis_title="Month",
    yaxis_title="Total Vehicles",
    barmode='group'
)

# Show the figure
fig.show()
