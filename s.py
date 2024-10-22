import altair as alt
import pandas as pd

# Example dataframe structure similar to yours
df = pd.DataFrame({
    'Operator': ['Operator 10', 'Operator 10', 'Operator 11', 'Operator 12', 'Operator 13'],  # Add your operator names
    'Workcenter': ['400A', '400A', '400B', '400B', '400A'],  # Add your workcenter names
    'Start_Time': [0, 0, 0, 0, 0],  # All operations start at 0 for simplicity
    'End_Time': [5, 3, 6, 7, 2]  # End times for each operator
})

# Group by Operator and Workcenter, getting the max End_Time for each group
df_grouped = df.groupby(['Operator', 'Workcenter'], as_index=False).agg({
    'End_Time': 'max'  # Max End_Time per operator per work center
})

# Define the correct order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Ensure workcenter is ordered correctly
df_grouped['Workcenter'] = pd.Categorical(df_grouped['Workcenter'], categories=workcenter_order, ordered=True)

# Base grouped bar chart (not stacked)
base_chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('Operator:N', title='Operator'),  # X axis is Operator for grouping
    y=alt.Y('End_Time:Q', title='End Time (Hours)'),  # Y axis is the max End_Time for each operator
    color=alt.Color('Operator:N', title='Operator'),  # Color by operator
    column=alt.Column('Workcenter:N', title='Workcenter', sort=workcenter_order)  # Grouped by work center
).properties(
    title="Operator Max End Time by Workcenter",
    width=100,  # Adjust width for each workcenter column
    height=400
)

# Calculate the top 3 maximum End_Time values overall for annotation
top_3_max = df_grouped.nlargest(3, 'End_Time')

# Annotations for the top 3 maximum times
annotations_top_3 = alt.Chart(top_3_max).mark_text(
    align='center', dy=-10, color='black'
).encode(
    x=alt.X('Operator:N'),
    y=alt.Y('End_Time:Q'),
    text=alt.Text('End_Time:Q', format='.2f'),
    column=alt.Column('Workcenter:N', sort=workcenter_order)
)

# Combine the base chart and the annotations
final_chart = base_chart + annotations_top_3

# Display the final chart
final_chart.show()