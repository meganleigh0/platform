import altair as alt
import pandas as pd

# Sample data preparation (Replace this with your actual dataframe all_dfs)
data = {
    'Program': ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C'],
    'Operator': ['Op1', 'Op2', 'Op1', 'Op3', 'Op2', 'Op1', 'Op3', 'Op4', 'Op2'],
    'WCAssigned': ['WC1', 'WC2', 'WC1', 'WC2', 'WC3', 'WC1', 'WC2', 'WC3', 'WC1'],
    'Criticality Rating': [1, 2, 1, 2, 1, 2, 1, 1, 2]
}
all_dfs = pd.DataFrame(data)

# Aggregations
operators_by_program = all_dfs.groupby('Program')['Operator'].nunique().reset_index()
operations_by_program = all_dfs.groupby('Program').size().reset_index(name='Total Operations')
ops_by_wc_program = all_dfs.groupby(['Program', 'WCAssigned']).size().reset_index(name='Operations')
criticality_by_program = all_dfs.groupby(['Program', 'Criticality Rating']).size().reset_index(name='Count')

# Chart: Unique Operators by Program
chart1 = alt.Chart(operators_by_program).mark_bar().encode(
    x='Program',
    y='Operator',
    color='Program',
    tooltip=['Program', 'Operator']
).properties(
    title='Unique Operators by Program'
)

# Chart: Total Operations by Program
chart2 = alt.Chart(operations_by_program).mark_bar().encode(
    x='Program',
    y='Total Operations',
    color='Program',
    tooltip=['Program', 'Total Operations']
).properties(
    title='Total Operations per Program'
)

# Chart: Operations by Work Center Assigned per Program
chart3 = alt.Chart(ops_by_wc_program).mark_bar().encode(
    x='WCAssigned',
    y='Operations',
    color='WCAssigned',
    tooltip=['Program', 'WCAssigned', 'Operations']
).properties(
    title='Operations by Work Center per Program'
).facet(
    facet='Program:N',
    columns=1
)

# Chart: Criticality Distribution per Program
chart4 = alt.Chart(criticality_by_program).mark_bar().encode(
    x='Criticality Rating:O',
    y='Count',
    color='Criticality Rating:N',
    tooltip=['Program', 'Criticality Rating', 'Count']
).properties(
    title='Criticality of Operations per Program'
).facet(
    facet='Program:N',
    columns=1
)

# Combine the charts into a single view
final_chart = (chart1 | chart2) & (chart3 & chart4)
final_chart.display()
