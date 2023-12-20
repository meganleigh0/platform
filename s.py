import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

# Assuming df is your DataFrame
# df = pd.read_csv('your_data.csv')  # Load your DataFrame

# Convert utilization to percentage
df['Utilization'] = df['Utilization'] * 100

# Aggregate utilization by plant
plant_utilization = df.groupby('plant')['Utilization'].mean().reset_index()

# Create a subplot
num_plants = len(plant_utilization['plant'].unique())
fig = sp.make_subplots(
    rows=2, cols=num_plants,
    subplot_titles=plant_utilization['plant'].unique(),
    specs=[[{"type": "indicator"}] * num_plants, [{"type": "bar"}] * num_plants]
)

# Add gauges for each plant
for i, plant in enumerate(plant_utilization['plant'].unique(), 1):
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=plant_utilization[plant_utilization['plant'] == plant]['Utilization'].iloc[0],
            title={'text': f"Plant {plant}"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ),
        row=1, col=i
    )

    # Add detailed bar chart for each plant by department
    department_utilization = df[df['plant'] == plant].groupby('Department')['Utilization'].mean().reset_index()
    fig.add_trace(
        go.Bar(
            x=department_utilization['Department'],
            y=department_utilization['Utilization'],
            name=f"Dept Utilization in {plant}"
        ),
        row=2, col=i
    )

# Update layout
fig.update_layout(
    title_text="Plant and Department Utilization Overview",
    height=600,
    showlegend=False
)

fig.show()
