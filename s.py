operations_data = []

for index, row in df_lim.iterrows():
    for operation in row['Operations']:
        operations_data.append({'Station': row['Station'], 'Department': operation[2], 'Hours': operation[0]})

operations_df = pd.DataFrame(operations_data)
total_hours_by_dept = operations_df.groupby('Department')['Hours'].sum().reset_index(name='Total Hours')
import plotly.express as px

fig = px.bar(total_hours_by_dept, x='Department', y='Total Hours',
             title='Total Operation Hours by Department',
             labels={'Total Hours': 'Total Operation Hours'},
             color='Total Hours',
             color_continuous_scale=px.colors.sequential.Viridis)
fig.show()
