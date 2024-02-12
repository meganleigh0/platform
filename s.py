# Group by station and assembly description and aggregate
grouped_df = df.groupby(['station', 'assembly_description']).agg(num_operations=('index', 'count'), total_hours=('hours', 'sum')).reset_index()

# Plot using Plotly
fig = px.bar(grouped_df, x='station', y='num_operations', color='assembly_description', hover_data=['total_hours'],
             labels={'num_operations': 'Number of Operations', 'total_hours': 'Total Hours'},
             title='Number of Operations by Station and Assembly Description',
             barmode='group')
fig.show()