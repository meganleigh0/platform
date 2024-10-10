import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Assuming you have a DataFrame 'df' with 'WorkCenter', 'WCAssigned', 'Difference', and 'PartNumber'

# Heatmap of Deviations
heatmap_df = df.groupby(['WorkCenter', 'WCAssigned']).size().reset_index(name='count')

fig_heatmap = px.density_heatmap(
    heatmap_df, 
    x='WorkCenter', 
    y='WCAssigned', 
    z='count', 
    title="Heatmap of Reassigned WorkCenters",
    labels={'WorkCenter': 'Planned WorkCenter', 'WCAssigned': 'Assigned WorkCenter'}
)
fig_heatmap.show()

# Sankey Diagram to visualize flow between WorkCenter and WCAssigned
# Create a list of unique work centers
all_workcenters = list(set(df['WorkCenter'].unique()).union(set(df['WCAssigned'].unique())))

# Create mappings from work center names to numerical indices for the sankey diagram
workcenter_map = {workcenter: i for i, workcenter in enumerate(all_workcenters)}

# Prepare the data for the Sankey diagram
df['WorkCenter_num'] = df['WorkCenter'].map(workcenter_map)
df['WCAssigned_num'] = df['WCAssigned'].map(workcenter_map)

# Prepare the links for the Sankey diagram
sankey_df = df.groupby(['WorkCenter_num', 'WCAssigned_num']).size().reset_index(name='value')

# Sankey Diagram
sankey_fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_workcenters
    ),
    link=dict(
        source=sankey_df['WorkCenter_num'],  # From planned work centers
        target=sankey_df['WCAssigned_num'],  # To assigned work centers
        value=sankey_df['value']  # How many operations were moved
    )
))

sankey_fig.update_layout(title_text="Flow of Operations from Planned to Assigned WorkCenters", font_size=10)
sankey_fig.show()