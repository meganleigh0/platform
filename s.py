all_dfs = pd.DataFrame(data)

# Define a custom sort order for WCAssigned
sort_order = ['WC1', 'WC2', 'WC3']

# Aggregations
hours_by_program = all_dfs.groupby('Program')['Hours'].sum().reset_index()
ops_by_wc_program = all_dfs.groupby(['Program', 'WCAssigned']).sum().reset_index()
ops_by_wc_program['WCAssigned'] = pd.Categorical(ops_by_wc_program['WCAssigned'], categories=sort_order, ordered=True)
ops_by_wc_program = ops_by_wc_program.sort_values(['Program', 'WCAssigned'])

# Chart: Total Hours by Program
chart1 = alt.Chart(hours_by_program).mark_bar().encode(
    x='Program',
    y='Hours',
    color='Program',
    tooltip=['Program', 'Hours']
).properties(
    title='Total Hours by Program'
)

# Chart: Operations by Work Center Assigned per Program with Annotations
chart3 = alt.Chart(ops_by_wc_program).mark_bar().encode(
    x=alt.X('WCAssigned', sort=sort_order),
    y=alt.Y('Hours', title='Total Hours'),
    color=alt.Color('WCAssigned', legend=None),
    tooltip=['Program', 'WCAssigned', 'Hours']
).properties(
    title='Total Hours by Work Center per Program'
).facet(
    facet='Program:N',
    columns=4  # Number of columns in the facet grid
).mark_text(
    align='center',
    baseline='middle',
    dy=-10  # Adjust vertical position relative to the bar
).encode(
    text='Hours'
)

# Combine the charts
final_chart = chart1 & chart3
final_chart.display()
