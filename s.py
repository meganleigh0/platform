import altair as alt

# Group by Operator and Workcenter, getting the max End_Time for each group
df_grouped = df.groupby(['Operator', 'Workcenter'], as_index=False).agg({'End_Time': 'max'})

# Define the correct order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', 
                    '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Ensure Workcenter is ordered correctly
df_grouped['Workcenter'] = pd.Categorical(df_grouped['Workcenter'], categories=workcenter_order, ordered=True)

# Create grouped bar chart (not stacked)
base_chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('Workcenter:N', title='Workcenter', sort=workcenter_order),
    y=alt.Y('End_Time:Q', title='End Time (Hours)'),  # Y axis is the max End_Time for each operator
    color=alt.Color('Operator:N', title='Operator'),  # Color by operator
    column='Workcenter:N'  # Group by Workcenter
).properties(
    title='Operator Max End Time by Workcenter',
    width=100,  # Adjust the width for each group
    height=400
)

# Calculate the top 3 maximum End_Time values overall for annotation
top3_max = df_grouped.nlargest(3, 'End_Time')

# Annotations for the top 3 maximum times
annotations_top_3 = alt.Chart(top3_max).mark_text(
    align='left', dx=3, dy=-5, color='black'
).encode(
    x=alt.X('Workcenter:N', sort=workcenter_order),
    y=alt.Y('End_Time:Q'),
    text=alt.Text('End_Time:Q', format='.2f')
)

# Combine the base chart and the annotations
final_chart = base_chart + annotations_top_3

# Display the final chart
final_chart.display()