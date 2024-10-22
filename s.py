import altair as alt
import pandas as pd

# Example dataframe structure
df = pd.DataFrame({
    'Operator': ['Operator 10', 'Operator 10', 'Operator 11', 'Operator 12', ...],  # Add your operator names
    'Workcenter': ['400A', '400A', '400B', '4001', ...],  # Add your workcenter names
    'OpNum': [1, 2, 3, 4, ...],  # Add your operation numbers
    'Start_Time': [1, 1.5, 2, 3, ...],  # Add your start times
    'End_Time': [5, 4.5, 6, 7, ...],  # Add your end times
})

# Group by Operator and Workcenter and get the max End_Time for each group
df_grouped = df.groupby(['Operator', 'Workcenter'], as_index=False).agg({
    'Start_Time': 'min',  # Start time of the first operation at that work center
    'End_Time': 'max'  # End time of the last operation at that work center
})

# Define the correct order for the work centers to reflect the assembly line order
workcenter_order = ['400A', '400B', '4001', '4002', '4003', '4004', '4005', '4006', '4007', '4008', '4009', '4010', '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Ensure workcenter is ordered correctly
df_grouped['Workcenter'] = pd.Categorical(df_grouped['Workcenter'], categories=workcenter_order, ordered=True)

# Ensure data is passed correctly to the chart
base_chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('Start_Time:Q', title='Start Time (Hours)', axis=alt.Axis(grid=False)),  # No grid lines
    x2='End_Time:Q',
    y=alt.Y('Operator:N', title='Operator'),
    color=alt.Color('Workcenter:N', title='Workcenter', sort=workcenter_order, scale=alt.Scale(scheme='category20'))
).facet(
    facet=alt.Facet('Workcenter:N', title='Workcenter', sort=workcenter_order)  # Facet by work center
).properties(
    title="Assembly Operator Man Assignment by Workcenter",
    width=150,  # Adjust width for each workcenter
    height=400,
    data=df_grouped  # Explicitly pass the dataframe
)

# Apply no grid lines configuration globally without layering
final_chart = base_chart.configure_view(
    strokeWidth=0  # No grid lines
)

# Display the final chart
final_chart.show()