import pandas as pd
import plotly.express as px

# Step 1: Group by Workcenter to calculate avg, max, and min deviations
# Calculate average deviation
avg_deviation = df.groupby('Workcenter')['Difference'].mean().reset_index(name='avg_deviation')

# Calculate max deviation
max_deviation = df.groupby('Workcenter')['Difference'].max().reset_index(name='max_deviation')

# Calculate min deviation
min_deviation = df.groupby('Workcenter')['Difference'].min().reset_index(name='min_deviation')

# Calculate total number of operations
total_ops = df.groupby('Workcenter')['Difference'].size().reset_index(name='total_ops')

# Step 2: Calculate the number of operations with no change (Difference == 0)
no_change_count = df[df['Difference'] == 0].groupby('Workcenter').size().reset_index(name='num_no_change')

# Step 3: Merge all calculated data into a single DataFrame
summary_df = avg_deviation.merge(max_deviation, on='Workcenter')
summary_df = summary_df.merge(min_deviation, on='Workcenter')
summary_df = summary_df.merge(total_ops, on='Workcenter')
summary_df = summary_df.merge(no_change_count, on='Workcenter', how='left')

# Fill NaN values in num_no_change with 0 (in case there were no operations with 0 difference for some workcenters)
summary_df['num_no_change'] = summary_df['num_no_change'].fillna(0)

# Step 4: Create a grouped bar chart showing average deviation and number of no-change operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='Workcenter', 
    y=['avg_deviation', 'num_no_change'],  # Show both deviation and stability metrics
    title="Impact of Deviations by Workcenter",
    labels={'avg_deviation': 'Average Deviation', 'num_no_change': 'No Change (Count)'},
    barmode='group',  # Group bars for better comparison
    height=600,
    width=1000
)

fig_grouped_bar.update_layout(
    xaxis_title="Planned Workcenter",
    yaxis_title="Deviation / No Change Count",
    showlegend=True,
    legend_title_text="Metrics"
)

fig_grouped_bar.show()