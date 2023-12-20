import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

# Assuming df is your DataFrame
# df = pd.read_csv('your_data.csv')  # Load your DataFrame

# Aggregate utilization by plant
plant_utilization = df.groupby('Plant')['Utilization'].mean().reset_index()

# Create a subplot
fig = sp.make_subplots(
    rows=2, cols=len(plant_utilization['Plant'].unique()),
    subplot_titles=plant_utilization['Plant'].unique(),
    specs=[[{"type": "indicator"}] * len(plant_utilization), [{"type": "bar"}] * len(plant_utilization)]
)

# Add gauges for each plant
for i, plant in enumerate(plant_utilization['Plant'].unique(), 1):
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=plant_utilization[plant_utilization['Plant'] == plant]['Utilization'].iloc[0],
            title={'text': f"Plant {plant}"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ),
        row=1, col=i
    )

    # Add detailed bar chart for each plant by department
    department_utilization = df[df['Plant'] == plant].groupby('Department')['Utilization'].mean().reset_index()
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
