import altair as alt

# Assuming each operator starts at time zero and the end time is their max End_Time
df_grouped['Start_Time'] = 0  # Add a column to represent the start time as zero

# Define the correct order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', 
                    '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Ensure Workcenter is ordered correctly
df_grouped['Workcenter'] = pd.Categorical(df_grouped['Workcenter'], categories=workcenter_order, ordered=True)

# Create a Gantt-like bar chart where each operator starts at 0 and ends at their End_Time
base_chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('Start_Time:Q', title='Time (Hours)', axis=alt.Axis(grid=False)),  # Start at zero
    x2='End_Time:Q',  # End time for each operator
    y=alt.Y('Workcenter:N', title='Workcenter', sort=workcenter_order),  # Workcenter on Y axis
    color=alt.Color('Operator:N', title='Operator'),  # Color by operator
    tooltip=['Operator:N', 'End_Time:Q']  # Show operator and time on hover
).properties(
    title='Operator Loading Chart by Workcenter',
    width=800,
    height=400
)

# Annotate the critical path (longest duration per WorkCenter)
critical_path = df_grouped.loc[df_grouped.groupby('Workcenter')['End_Time'].idxmax()]  # Critical path as longest End_Time

annotations_cp = alt.Chart(critical_path).mark_text(
    align='left', dx=3, dy=-5, color='black'
).encode(
    x=alt.X('End_Time:Q'),
    y=alt.Y('Workcenter:N', sort=workcenter_order),
    text=alt.Text('End_Time:Q', format='.2f')
)

# Combine the base chart and the critical path annotations
final_chart = base_chart + annotations_cp

# Display the final chart
final_chart.display()