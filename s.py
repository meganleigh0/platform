# Unique operators by program
operators_by_program = all_dfs.groupby('Program')['Operator'].nunique().reset_index()

# Total operations by program
operations_by_program = all_dfs.groupby('Program').size().reset_index(name='Total Operations')

# Operations by work center and program
ops_by_wc_program = all_dfs.groupby(['Program', 'WCAssigned']).size().reset_index(name='Operations')

# Criticality distribution by program
criticality_by_program = all_dfs.groupby(['Program', 'Criticality Rating']).size().reset_index(name='Count')
chart1 = alt.Chart(operators_by_program).mark_bar().encode(
    x='Program',
    y='Operator',
    color=alt.condition(single_select, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['Program', 'Operator']
).properties(
    title='Unique Operators by Program'
).add_selection(
    single_select
)
chart2 = alt.Chart(operations_by_program).mark_bar().encode(
    x='Program',
    y='Total Operations',
    color=alt.condition(single_select, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['Program', 'Total Operations']
).properties(
    title='Total Operations by Program'
)
chart3 = alt.Chart(ops_by_wc_program).mark_bar().encode(
    x='WCAssigned',
    y='Operations',
    color=alt.Color('WCAssigned', legend=None),
    tooltip=['WCAssigned', 'Operations']
).transform_filter(
    single_select
).properties(
    title='Operations by Work Center per Selected Program'
)
chart4 = alt.Chart(criticality_by_program).mark_bar().encode(
    x='Criticality Rating',
    y='Count',
    color='Criticality Rating',
    tooltip=['Criticality Rating', 'Count']
).transform_filter(
    single_select
).properties(
    title='Criticality of Operations per Selected Program'
)
final_chart = alt.concat(chart1, chart2, chart3, chart4, columns=2).resolve_scale(color='independent')
final_chart.display()
