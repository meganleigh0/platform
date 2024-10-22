import altair as alt
import pandas as pd

# Assuming you have a similar dataframe structure already
df = pd.DataFrame({
    'Operator': ['Operator 10', 'Operator 11', 'Operator 12', ...],  # Add your operator names
    'Workcenter': ['400A', '400A', '400B', ...],  # Add your workcenter names
    'Start_Time': [1, 2, 3, ...],  # Add your start times
    'End_Time': [5, 6, 7, ...],  # Add your end times
    'Hours': [4, 4, 4, ...]  # Duration of operation
})

# Sort the dataframe by workcenter and start time for clarity
df_sorted = df.sort_values(by=['Workcenter', 'Start_Time'])

# Base chart with bars for each operator, representing their time at each workcenter
chart = alt.Chart(df_sorted).mark_bar().encode(
    x=alt.X('Start_Time:Q', title='Start Time (Hours)'),
    x2='End_Time:Q',
    y=alt.Y('Operator:N', title='Operator'),
    color=alt.Color('Workcenter:N', title='Workcenter')
).properties(
    title="Assembly Operator Man Assignment",
    width=800,
    height=600
)

# Calculate the max completion time for each operator (this can be done externally)
max_times = df_sorted.groupby('Operator')['End_Time'].max().reset_index()

# Annotations for max times per operator
annotations = alt.Chart(max_times).mark_text(align='left', dx=3).encode(
    x=alt.X('End_Time:Q'),
    y=alt.Y('Operator:N'),
    text=alt.Text('End_Time:Q')
)

# Combine the chart and annotations
final_chart = chart + annotations

# Display the final chart
final_chart.show()