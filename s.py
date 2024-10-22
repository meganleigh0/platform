import altair as alt
import pandas as pd

# Example dataframe structure
df = pd.DataFrame({
    'Operator': ['Operator 10', 'Operator 11', 'Operator 12', ...],  # Add your operator names
    'Workcenter': ['400A', '400A', '400B', ...],  # Add your workcenter names
    'Start_Time': [1, 2, 3, ...],  # Add your start times
    'End_Time': [5, 6, 7, ...],  # Add your end times
    'Hours': [4, 4, 4, ...]  # Duration of operation
})

# Sort the dataframe by workcenter and start time
df_sorted = df.sort_values(by=['Workcenter', 'Start_Time'])

# Define the order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Base chart with unique colors for each workcenter
base_chart = alt.Chart(df_sorted).mark_bar().encode(
    x=alt.X('Start_Time:Q', title='Start Time (Hours)'),
    x2='End_Time:Q',
    y=alt.Y('Operator:N', title='Operator'),
    color=alt.Color('Workcenter:N', title='Workcenter', sort=workcenter_order, scale=alt.Scale(scheme='category20')),
    order=alt.Order('Workcenter:N', sort='ascending')
).properties(
    title="Assembly Operator Man Assignment by Workcenter",
    width=900,
    height=600
)

# Calculate the top 3 maximum End_Time values overall
top_3_max = df_sorted.nlargest(3, 'End_Time')

# Annotations for the top 3 maximum times
annotations_top_3 = alt.Chart(top_3_max).mark_text(
    align='left', dx=5, dy=-5, color='black'
).encode(
    x=alt.X('End_Time:Q'),
    y=alt.Y('Operator:N'),
    text=alt.Text('End_Time:Q', format='.2f')
)

# Combine the base chart and the annotations
final_chart = base_chart + annotations_top_3

# Display the final chart
final_chart.show()