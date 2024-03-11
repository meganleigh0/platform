# Resetting the index for easier manipulation and to use 'Variant' in visualizations
df_reset = all_operations_df.reset_index()

# Aggregating data directly in groupby
variant_metrics = df_reset.groupby(['Variant', 'Operation Description', 'Name']).agg({
    'Hours': ['sum', 'mean', 'count']
}).reset_index()

# Renaming columns for clarity
variant_metrics.columns = ['Variant', 'Operation Description', 'Name', 'TotalHours', 'AvgHours', 'OperationsCount']

# Proceeding to visualization with the corrected DataFrame

import altair as alt

# Total Hours per Operation by Variant
chart_total_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x='Variant:N',
    y='TotalHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Total Hours per Operation by Variant")

# Average Hours per Operation by Variant
chart_avg_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x='Variant:N',
    y='AvgHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Average Hours per Operation by Variant")

(chart_total_hours | chart_avg_hours).display()

import altair as alt

# Total Hours per Operation by Variant
chart_total_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x='Variant:N',
    y='TotalHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Total Hours per Operation by Variant")

# Average Hours per Operation by Variant
chart_avg_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x='Variant:N',
    y='AvgHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Average Hours per Operation by Variant")

(chart_total_hours | chart_avg_hours).display()

# Department Involvement in Operations
chart_department_involvement = alt.Chart(variant_metrics).mark_bar().encode(
    x='OperationsCount:Q',
    y=alt.Y('Name:N', sort='-x'),
    color='Variant:N',
    tooltip=['Name', 'OperationsCount', 'Variant']
).properties(width=600, title="Department Involvement in Operations Across Variants")

chart_department_involvement.display()

