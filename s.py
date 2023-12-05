import pandas as pd
import plotly.express as px

# Simulated data based on the user's description
data = {
    "Interaction": ["Plant 1 Status"] * 6,
    "Timestamp": [0.00, 0.00, 0.00, 2.00, 3.00, 4.00],
    "Turret_Completed": [0, 0, 0, 1, 1, 3],
    "Turret_Processing": [1, 2, 3, 2, 3, 1],
    "Hull_Completed": [0, 0, 0, 0, 1, 2],
    "Hull_Processing": [1, 2, 3, 3, 2, 3]
}

df = pd.DataFrame(data)

# Creating an animated bar chart using Plotly
fig = px.bar(df, 
             x="Timestamp", 
             y=["Turret_Completed", "Turret_Processing", "Hull_Completed", "Hull_Processing"],
             labels={"value": "Count", "variable": "Status"},
             animation_frame="Timestamp",
             range_y=[0, df[["Turret_Completed", "Turret_Processing", "Hull_Completed", "Hull_Processing"]].values.max() + 1],
             title="Simulation Data Over Time")

fig.update_layout(barmode='group')
fig.show()
