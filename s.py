# Aggregations
operators_by_program = all_dfs.groupby('Program')['Operator'].nunique().reset_index()
operations_by_program = all_dfs.groupby('Program').size().reset_index(name='Total Operations')
ops_by_wc_program = all_dfs.groupby(['Program', 'WCAssigned']).size().reset_index(name='Operations')
criticality_by_program = all_dfs.groupby(['Program', 'Criticality Rating']).size().reset_index(name='Count')

# Sorting operations by work center within each program
ops_by_wc_program['WCAssigned'] = pd.Categorical(ops_by_wc_program['WCAssigned'], categories=sort_order, ordered=True)
ops_by_wc_program = ops_by_wc_program.sort_values(['Program', 'WCAssigned'])

# Chart: Operations by Work Center Assigned per Program
chart3 = alt.Chart(ops_by_wc_program).mark_bar().encode(
    x=alt.X('WCAssigned', sort=sort_order),
    y='Operations',
    color=alt.Color('WCAssigned', legend=None),
    tooltip=['Program', 'WCAssigned', 'Operations']
).properties(
    title='Operations by Work Center per Program'
).facet(
    facet='Program:N',
    columns=1
)

# Display the chart
chart3.display()
