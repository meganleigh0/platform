import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Example DataFrame (Replace this with your actual data)
data = {
    'WCAssigned': ['400A', '400B', '4001', '4002', '4003', '400A', '4002'],
    'WorkCenter': ['400A', '400B', '4003', '4002', '4001', '4002', '400B']
}
df = pd.DataFrame(data)

# Step 1: Create a mapping of the WorkCenters to numerical values
# Sort the unique work centers to assign consistent encoding based on order
unique_workcenters = sorted(set(df['WCAssigned'].unique()).union(df['WorkCenter'].unique()))
workcenter_map = {center: i for i, center in enumerate(unique_workcenters)}

# Step 2: Encode the WCAssigned and WorkCenter columns to numerical values
df['WCAssigned_Num'] = df['WCAssigned'].map(workcenter_map)
df['WorkCenter_Num'] = df['WorkCenter'].map(workcenter_map)

# Step 3: Calculate the absolute difference between the two columns
df['Difference'] = np.abs(df['WCAssigned_Num'] - df['WorkCenter_Num'])

# Step 4: Plotly Scatter Plot
scatter_fig = px.scatter(
    df,
    x='WCAssigned_Num',
    y='WorkCenter_Num',
    color='Difference',
    hover_data=['WCAssigned', 'WorkCenter'],
    color_continuous_scale='Viridis',
    title="WCAssigned vs WorkCenter with Difference Magnitude"
)
scatter_fig.update_layout(xaxis_title='WCAssigned (Encoded)', yaxis_title='WorkCenter (Encoded)')
scatter_fig.show()

# Step 5: Plotly Bar Chart Showing the Differences
bar_fig = px.bar(
    df,
    x=df.index,
    y='Difference',
    text='Difference',
    hover_data=['WCAssigned', 'WorkCenter'],
    title='Difference between WCAssigned and WorkCenter'
)
bar_fig.update_layout(xaxis_title='Index', yaxis_title='Difference (Encoded Values)')
bar_fig.show()

# Step 6: Print the DataFrame with the calculated differences
print(df[['WCAssigned', 'WorkCenter', 'WCAssigned_Num', 'WorkCenter_Num', 'Difference']])