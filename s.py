# Assuming all_operations_df is already defined with the MultiIndex structure

# Resetting the index for easier manipulation and to use 'Variant' in our visualizations
df_reset = all_operations_df.reset_index()

# Aggregating data while considering the 'Variant'
variant_metrics = df_reset.groupby(['Variant', 'Operation Description', 'Name']).agg(
    TotalHours=pd.NamedAgg(column='Hours', aggfunc='sum'),
    AvgHours=pd.NamedAgg(column='Hours', aggfunc='mean'),
    OperationsCount=pd.NamedAgg(column='Operation Description', aggfunc='count')
).reset_index()

# Total Hours per Operation by Variant
chart_total_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x=alt.X('Variant:N', sort=alt.EncodingSortField(field="TotalHours", op="sum", order='descending')),
    y='TotalHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Total Hours per Operation by Variant")

# Average Hours per Operation by Variant
chart_avg_hours = alt.Chart(variant_metrics).mark_bar().encode(
    x=alt.X('Variant:N', sort=alt.EncodingSortField(field="AvgHours", op="mean", order='descending')),
    y='AvgHours:Q',
    color='Variant:N',
    tooltip=['Variant', 'Operation Description', 'TotalHours', 'AvgHours'],
    column=alt.Column('Operation Description:N', header=alt.Header(labelAngle=-90, titleOrient="top"))
).properties(width=150, height=200, title="Average Hours per Operation by Variant")

chart_total_hours | chart_avg_hours

# Department Involvement in Operations
chart_department_involvement = alt.Chart(variant_metrics).mark_bar().encode(
    x='sum(OperationsCount):Q',
    y=alt.Y('Name:N', sort=alt.EncodingSortField(field="OperationsCount", op="sum", order='descending')),
    color='Variant:N',
    tooltip=['Name', 'sum(OperationsCount)', 'Variant']
).properties(width=600, title="Department Involvement in Operations Across Variants")

chart_department_involvement.display()