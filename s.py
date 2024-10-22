# Count unique operators per program
unique_operators = all_dfs.groupby('Program')['Operator'].nunique().reset_index()

# Count total operations per program
total_operations = all_dfs.groupby('Program').size().reset_index(name='Total Operations')
fig_unique_ops = px.bar(unique_operators, x='Program', y='Operator', 
                        title='Unique Operators per Program',
                        labels={'Operator': 'Count of Unique Operators'})
fig_unique_ops.show()
fig_total_ops = px.bar(total_operations, x='Program', y='Total Operations', 
                       title='Total Operations per Program')
fig_total_ops.show()
