# Faceted bar chart to show hours per work center, faceted by program
fig = px.bar(all_dfs, x='WCAssigned', y='Hours',
             facet_col='Program', facet_col_wrap=2,
             color='WCAssigned', text='Hours',
             labels={"WCAssigned": "Work Center", "Hours": "Total Hours"},
             title="Distribution of Hours by Work Center and Program")

# Improve layout
fig.update_layout(
    showlegend=False,
    yaxis_title='Total Hours',
    plot_bgcolor='white'
)

# Set uniform axis ranges for better comparison
fig.update_yaxes(matches=None, showticklabels=True)

# Customize facet titles
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# Display the plot
fig.show()
