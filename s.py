import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    'plant': ['Plant1', 'Plant1', 'Plant2', 'Plant2'],
    'department': ['Dept1', 'Dept2', 'Dept1', 'Dept2'],
    'month': ['Jan', 'Jan', 'Jan', 'Jan'],
    'act_hours': [200, 150, 180, 160],
    'est_hours': [190, 160, 175, 165]
}
df = pd.DataFrame(data)

# Plot by Department
fig_dept = px.scatter(df, x='est_hours', y='act_hours', color='department', 
                      title='Actual vs Estimated Hours by Department',
                      labels={'est_hours': 'Estimated Hours', 'act_hours': 'Actual Hours'},
                      hover_data=['month'])
fig_dept.show()

# Aggregate by Plant and Plot
df_plant = df.groupby(['plant']).agg({'act_hours': 'sum', 'est_hours': 'sum'}).reset_index()
fig_plant = px.scatter(df_plant, x='est_hours', y='act_hours', color='plant',
                       title='Actual vs Estimated Hours by Plant',
                       labels={'est_hours': 'Estimated Hours', 'act_hours': 'Actual Hours'})
fig_plant.show()