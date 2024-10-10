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

# Step 3: Calculate the number of operations that did change (Difference != 0)
changed_count = df[df['Difference'] != 0].groupby('Workcenter').size().reset_index(name='num_changed')

# Step 4: Merge all calculated data into a single DataFrame
summary_df = avg_deviation.merge(max_deviation, on='Workcenter')
summary_df = summary_df.merge(min_deviation, on='Workcenter')
summary_df = summary_df.merge(total_ops, on='Workcenter')
summary_df = summary_df.merge(no_change_count, on='Workcenter', how='left')
summary_df = summary_df.merge(changed_count, on='Workcenter', how='left')

# Fill NaN values in num_no_change and num_changed with 0 (in case there were no operations with 0 difference for some workcenters)
summary_df['num_no_change'] = summary_df['num_no_change'].fillna(0)
summary_df['num_changed'] = summary_df['num_changed'].fillna(0)

# Step 5: Sort the work centers in a specific order (e.g., 400A, 400B, 401, etc.)
# Define the correct order of Workcenters
workcenter_order = ['400A', '400B', '401', '402', '403', '404', '405', '406', '407', '408', '409', '4010', 
                    '4011', '4012', '4013', '4014', '4015', '4016', '4017']

# Sort the DataFrame based on the order of Workcenters
summary_df['Workcenter'] = pd.Categorical(summary_df['Workcenter'], categories=workcenter_order, ordered=True)
summary_df = summary_df.sort_values('Workcenter')

# Step 6: Create a grouped bar chart showing average deviation, number of no-change operations, and number of changed operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='Workcenter', 
    y=['avg_deviation', 'num_no_change', 'num_changed'],  # Show deviation and both types of operations
    title="Impact of Deviations by Workcenter",
    labels={'avg_deviation': 'Average Deviation', 'num_no_change': 'No Change (Count)', 'num_changed': 'Changed Operations (Count)'},
    barmode='group',  # Group bars for better comparison
    height=600,
    width=1000
)

# Step 7: Add annotations to the bars for better readability
for bar in fig_grouped_bar.data:
    bar.text = bar.y
    bar.textposition = 'outside'

# Final layout adjustments
fig_grouped_bar.update_layout(
    xaxis_title="Planned Workcenter",
    yaxis_title="Deviation / Operation Count",
    showlegend=True,
    legend_title_text="Metrics",
    uniformtext_minsize=8, 
    uniformtext_mode='hide'
)

# Display the figure
fig_grouped_bar.show()