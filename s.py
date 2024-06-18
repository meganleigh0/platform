import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    'plant': ['Plant1', 'Plant1', 'Plant2', 'Plant2', 'Plant1', 'Plant1', 'Plant2', 'Plant2'],
    'department': ['Dept1', 'Dept2', 'Dept1', 'Dept2', 'Dept1', 'Dept2', 'Dept1', 'Dept2'],
    'month': ['Jan', 'Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Feb'],
    'act_hours': [200, 150, 180, 160, 210, 165, 190, 170],
    'est_hours': [190, 160, 175, 165, 200, 150, 185, 175]
}
df = pd.DataFrame(data)

# Melt the DataFrame to make it suitable for a grouped bar chart
df_melted = df.melt(id_vars=['plant', 'department', 'month'], value_vars=['act_hours', 'est_hours'],
                    var_name='Type', value_name='Hours')

# Create a grouped bar chart
fig = px.bar(df_melted, x='department', y='Hours', color='Type', barmode='group',
             facet_col='month', title='Actual vs Estimated Hours by Department Each Month',
             labels={'department': 'Department', 'Hours': 'Hours'},
             category_orders={"month": ["Jan", "Feb"]})  # Adjust category_orders based on your months
fig.show()