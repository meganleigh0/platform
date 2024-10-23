import pandas as pd
import plotly.graph_objects as go

# Original data with cycle times
data = {
    "Program": ["Program A", "Program B", "Program C", "Program D"],
    "T Op Count": [351, 346, 346, 358],
    "T Op Hours": [155.75, 155.51, 153.13, 147.1],
    "T Cycle Time": [81.12, 81.12, 80.88, 76.56],  # in minutes
    "H Op Count": [576, 576, 575, 502],
    "H Op Hours": [201.72, 202.84, 201.62, 187.42],
    "H Cycle Time": [111.42, 106.38, 111.42, 109.44],  # in minutes
}

df_programs = pd.DataFrame(data)

# Sample scheduled quantities per month for each program
# Replace this with your actual scheduled data
schedule_data = {
    'Program': ['Program A', 'Program B', 'Program C', 'Program D'] * 6,
    'Month': ['2023-10', '2023-10', '2023-10', '2023-10',
              '2023-11', '2023-11', '2023-11', '2023-11',
              '2023-12', '2023-12', '2023-12', '2023-12',
              '2024-01', '2024-01', '2024-01', '2024-01',
              '2024-02', '2024-02', '2024-02', '2024-02',
              '2024-03', '2024-03', '2024-03', '2024-03'],
    'Scheduled_T_Units': [50, 60, 40, 70, 55, 65, 45, 75, 60, 70, 50, 80, 65, 75, 55, 85, 70, 80, 60, 90, 75, 85, 65, 95],
    'Scheduled_H_Units': [80, 90, 70, 100, 85, 95, 75, 105, 90, 100, 80, 110, 95, 105, 85, 115, 100, 110, 90, 120, 105, 115, 95, 125],
}

df_schedule = pd.DataFrame(schedule_data)

# Convert 'Month' to datetime
df_schedule['Month'] = pd.to_datetime(df_schedule['Month'], format='%Y-%m')

# Merge the cycle times into the schedule DataFrame
df_schedule = df_schedule.merge(
    df_programs[['Program', 'T Cycle Time', 'H Cycle Time']],
    on='Program',
    how='left'
)

# Calculate the predicted T and H operational hours
df_schedule['Predicted_T_Op_Hours'] = (
    df_schedule['Scheduled_T_Units'] * df_schedule['T Cycle Time'] / 60
)  # Convert minutes to hours

df_schedule['Predicted_H_Op_Hours'] = (
    df_schedule['Scheduled_H_Units'] * df_schedule['H Cycle Time'] / 60
)  # Convert minutes to hours

# Sum up the total predicted operational hours per month
df_monthly = df_schedule.groupby('Month').agg({
    'Predicted_T_Op_Hours': 'sum',
    'Predicted_H_Op_Hours': 'sum'
}).reset_index()

# Calculate total predicted operational hours
df_monthly['Total_Predicted_Op_Hours'] = (
    df_monthly['Predicted_T_Op_Hours'] + df_monthly['Predicted_H_Op_Hours']
)

# Calculate man-loading requirements (number of personnel required)
df_monthly['Man_Loading_Requirement'] = (
    df_monthly['Total_Predicted_Op_Hours'] / 120
)  # Assuming 120 hours per person per month

# Prepare data for plotting
df_melted = df_monthly.melt(
    id_vars=['Month', 'Man_Loading_Requirement'],
    value_vars=['Predicted_T_Op_Hours', 'Predicted_H_Op_Hours'],
    var_name='Operation Type',
    value_name='Operational Hours'
)

# Map operation types to more readable labels
df_melted['Operation Type'] = df_melted['Operation Type'].map({
    'Predicted_T_Op_Hours': 'T Operations',
    'Predicted_H_Op_Hours': 'H Operations'
})

# Convert 'Month' to string format for plotting
df_melted['Month_str'] = df_melted['Month'].dt.strftime('%Y-%m')
df_monthly['Month_str'] = df_monthly['Month'].dt.strftime('%Y-%m')

# Define capacity line (assuming maximum capacity is based on available personnel)
available_personnel = 10  # Adjust based on actual number of personnel
max_capacity_per_month = available_personnel * 120  # 120 hours per person per month

# Create the visualization
fig = go.Figure()

# Add bar traces for T and H operations
for operation in df_melted['Operation Type'].unique():
    df_op = df_melted[df_melted['Operation Type'] == operation]
    fig.add_trace(go.Bar(
        x=df_op['Month_str'],
        y=df_op['Operational Hours'],
        name=operation,
        text=df_op['Operational Hours'].round(2),
        textposition='auto'
    ))

# Add a line trace for total operational hours
fig.add_trace(go.Scatter(
    x=df_monthly['Month_str'],
    y=df_monthly['Total_Predicted_Op_Hours'],
    mode='lines+markers',
    name='Total Operational Hours',
    line=dict(color='black', width=2, dash='dash'),
    marker=dict(size=8),
    hovertemplate='Total: %{y:.2f} hrs<br>Date: %{x}'
))

# Add a line for capacity
fig.add_trace(go.Scatter(
    x=df_monthly['Month_str'],
    y=[max_capacity_per_month] * len(df_monthly),
    mode='lines',
    name='Maximum Capacity',
    line=dict(color='red', width=2),
    hoverinfo='skip'
))

# Add annotations for man-loading requirements
for idx, row in df_monthly.iterrows():
    fig.add_annotation(
        x=row['Month_str'],
        y=row['Total_Predicted_Op_Hours'] + 50,  # Adjust position as needed
        text='Req. Personnel: {:.1f}'.format(row['Man_Loading_Requirement']),
        showarrow=False,
        font=dict(size=12, color='black'),
        align='center'
    )

# Update layout for better aesthetics
fig.update_layout(
    title='Predicted Operational Hours and Man-Loading Requirements',
    xaxis_title='Month',
    yaxis_title='Operational Hours',
    legend_title='Operation Type',
    barmode='stack',
    template='plotly_white',
    xaxis=dict(
        tickmode='array',
        tickvals=df_monthly['Month_str'],
        ticktext=df_monthly['Month'].dt.strftime('%b %Y')
    ),
    hovermode='x unified',
)

# Show the figure
fig.show()