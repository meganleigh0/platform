the max End_Time for each group
df_grouped = df.groupby(['Operator', 'Workcenter'], as_index=False).agg({
    'Start_Time': 'min',  # Start time of the first operation at that work center
    'End_Time': 'max'  # End time of the last operation at that work center
})

# Define the order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Base chart with unique colors for each workcenter
base_chart = alt.Chart(df_grouped).mark_bar().encode(
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
top_3_max = df_grouped.nlargest(3, 'End_Time')

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