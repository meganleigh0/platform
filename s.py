import plotly.express as px
import pandas as pd

# Assuming df is your DataFrame

# Convert 'Source' to datetime to sort it correctly in the plot
df['Source'] = pd.to_datetime(df['Source'], format='%B_%Y')

# Sort the DataFrame by Source to ensure chronological plotting
df.sort_values('Source', inplace=True)

# Create a stacked bar chart
fig = px.bar(df, 
             x='Source', 
             y='EstimatedHours', 
             color='DEPT', 
             title='Estimated Hours by Department across Sources',
             labels={'Source': 'Report Month', 'EstimatedHours': 'Hours'},
             facet_col='Plant', 
             facet_col_wrap=3, # Adjust based on how many plants there are
             category_orders={"Source": sorted(df['Source'].unique())}) # Ensure chronological order

# Improve layout
fig.update_layout(
    xaxis_title='Report Month',
    yaxis_title='Estimated Hours',
    xaxis_tickformat='%b %Y',  # Format the ticks to show abbreviated month and year
    xaxis_tickangle=-45,
    barmode='stack'
)

fig.show()
