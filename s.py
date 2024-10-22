
import pandas as pd
import plotly.graph_objects as go

# Data from the image, reorganized into a dictionary
data = {
    "Program": ["Program A", "Program B", "Program C", "Program D"],
    "T Op Count": [351, 346, 346, 358],
    "T Op Hours": [155.75, 155.51, 153.13, 147.1],
    "T Cycle Time": [81.12, 81.12, 80.88, 76.56],
    "H Op Count": [576, 576, 575, 502],
    "H Op Hours": [201.72, 202.84, 201.62, 187.42],
    "H Cycle Time": [111.42, 106.38, 111.42, 109.44],
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Create a Plotly table
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Program, df["T Op Count"], df["T Op Hours"], df["T Cycle Time"], 
                       df["H Op Count"], df["H Op Hours"], df["H Cycle Time"]],
               fill_color='lavender',
               align='left'))
])

# Add a title to the figure
fig.update_layout(title="Operational Summary by Program")

# Show the figure
fig.show()