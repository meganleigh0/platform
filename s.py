import plotly.express as px

# Ensure you have Plotly installed, or install it via pip install plotly

# Group by Station and PartNumber for the sum of TotalHours
grouped_data = df.groupby(['Station', 'PartNumber'])['TotalHours'].sum().reset_index()

# Creating the bar chart with Plotly
fig = px.bar(grouped_data, 
             x='Station', 
             y='TotalHours', 
             color='PartNumber', 
             barmode='group',
             text='TotalHours',
             hover_data=['Station', 'PartNumber', 'TotalHours'],
             labels={'TotalHours': 'Total Hours', 'Station': 'Station', 'PartNumber': 'Assembly'},
             title='Total Hours of Operations by Station and Assembly')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.update_layout(xaxis_tickangle=-45)

fig.show()