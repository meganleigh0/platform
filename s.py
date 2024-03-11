# Total Hours per Operation by Variant
chart_total_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x=alt.X('Variant:N', title='Variant'),
    y=alt.Y('TotalHours:Q', title='Total Hours'),
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours']
).properties(width=600, height=200, title="Total Hours per Operation by Variant")

# Display the chart
chart_total_hours.display()

# Department Involvement in Operations
chart_department_involvement = alt.Chart(variant_metrics).mark_bar().encode(
    x=alt.X('OperationsCount:Q', title='Operations Count'),
    y=alt.Y('Name:N', sort='-x', title='Department Name'),
    color='Variant:N',
    tooltip=['Name', 'OperationsCount', 'Variant']
).properties(width=600, title="Department Involvement in Operations Across Variants")

chart_department_involvement.display()