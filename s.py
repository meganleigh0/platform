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

# Base chart with bars for each operator, representing their time at each workcenter
base_chart = alt.Chart(df_sorted).mark_bar().encode(
    x=alt.X('Start_Time:Q', title='Start Time (Hours)'),
    x2='End_Time:Q',
    y=alt.Y('Operator:N', title='Operator'),
    color=alt.Color('Workcenter:N', title='Workcenter', scale=alt.Scale(scheme='tableau20'))
).properties(
    title="Assembly Operator Man Assignment by Workcenter",
    width=800,
    height=600
)

# Calculate the max completion time per workcenter and overall
max_per_workcenter = df_sorted.groupby('Workcenter')['End_Time'].max().reset_index()
max_overall = df_sorted['End_Time'].max()

# Annotations for max times per workcenter
annotations_workcenter = alt.Chart(max_per_workcenter).mark_text(align='left', dx=5, dy=-5, color='black').encode(
    x=alt.X('End_Time:Q'),
    y=alt.Y('Workcenter:N'),
    text=alt.Text('End_Time:Q', format='.1f')
)

# Annotation for the overall max value
annotations_max_overall = alt.Chart(pd.DataFrame({'End_Time': [max_overall]})).mark_rule(color='red', strokeDash=[5, 5]).encode(
    x='End_Time:Q'
) + alt.Chart(pd.DataFrame({'End_Time': [max_overall], 'label': ['Max Overall']})).mark_text(
    align='left', dx=3, dy=-5, color='red'
).encode(
    x='End_Time:Q',
    text='label:N'
)

# Combine the chart and annotations
final_chart = base_chart + annotations_workcenter + annotations_max_overall

# Display the final chart
final_chart.show()