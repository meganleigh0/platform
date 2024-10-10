import pandas as pd
import plotly.express as px

# Calculate summary statistics for each Workcenter
# Group by Workcenter and calculate average, max, min deviation and total operations
summary_df = df.groupby('Workcenter').agg(
    avg_deviation=('Difference', 'mean'),
    max_deviation=('Difference', 'max'),
    min_deviation=('Difference', 'min'),
    total_ops=('Difference', 'size')
).reset_index()

# Calculate the number of operations with no change (Difference = 0)
no_change_df = df[df['Difference'] == 0].groupby('Workcenter').size().reset_index(name='num_no_change')

# Merge the no_change_df back with summary_df to get the complete statistics
summary_df = summary_df.merge(no_change_df, on='Workcenter', how='left')

# Fill NaN values in num_no_change with 0 (in case there were no operations with 0 difference for some workcenters)
summary_df['num_no_change'] = summary_df['num_no_change'].fillna(0)

# Create a grouped bar chart showing average deviation and number of no-change operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='Workcenter', 
    y=['avg_deviation', 'num_no_change'],  # Show both deviation and stability metrics