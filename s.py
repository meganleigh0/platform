import pandas as pd
import plotly.express as px

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
    'Program': ['Program A', 'Program B', 'Program C', 'Program D'] * 3,
    'Month': ['October', 'October', 'October', 'October',
              'November', 'November', 'November', 'November',
              'December', 'December', 'December', 'December'],
    'Scheduled_T_Units': [50, 60, 40, 70, 55, 65, 45, 75, 60, 70, 50, 80],
    'Scheduled_H_Units': [80, 90, 70, 100, 85, 95, 75, 105, 90, 100, 80, 110]
}

df_schedule = pd.DataFrame(schedule_data)

# Merge the cycle times into the schedule DataFrame
df_schedule = df_schedule.merge(df_programs[['Program', 'T Cycle Time', 'H Cycle Time']], on='Program', how='left')

# Calculate the predicted T and H operational hours
df_schedule['Predicted_T_Op_Hours'] = (df_schedule['Scheduled_T_Units'] * df_schedule['T Cycle Time']) / 60  # Convert minutes to hours
df_schedule['Predicted_H_Op_Hours'] = (df_schedule['Scheduled_H_Units'] * df_schedule['H Cycle Time']) / 60  # Convert minutes to hours

# Sum up the total predicted operational hours per month
df_monthly = df_schedule.groupby('Month').agg({
    'Predicted_T_Op_Hours': 'sum',
    'Predicted_H_Op_Hours': 'sum'
}).reset_index()

# Melt the DataFrame for easier plotting
df_melted = df_monthly.melt(id_vars='Month', value_vars=['Predicted_T_Op_Hours', 'Predicted_H_Op_Hours'],
                            var_name='Operation Type', value_name='Operational Hours')

# Map operation types to more readable labels
df_melted['Operation Type'] = df_melted['Operation Type'].map({
    'Predicted_T_Op_Hours': 'T Operations',
    'Predicted_H_Op_Hours': 'H Operations'
})

# Create the visualization
fig = px.bar(df_melted, x='Month', y='Operational Hours', color='Operation Type',
             title='Predicted Operational Hours per Month',
             labels={'Operational Hours': 'Operational Hours', 'Operation Type': 'Operation Type'},
             barmode='group',
             text='Operational Hours')

# Update layout for better aesthetics
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Operational Hours',
    legend_title='Operation Type',
    template='plotly_white',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Add data labels
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# Show the figure
fig.show()