import pandas as pd
import plotly.express as px

# Step 1: Group by Workcenter and calculate avg, max, and min deviations ONLY for operations that moved (Difference != 0)
moved_operations = df[df['Difference'] != 0]

# Calculate average deviation for moved operations
avg_deviation_moved = moved_operations.groupby('Workcenter')['Difference'].mean().reset_index(name='avg_deviation_moved')

# Calculate max deviation for moved operations
max_deviation_moved = moved_operations.groupby('Workcenter')['Difference'].max().reset_index(name='max_deviation_moved')

# Calculate min deviation for moved operations
min_deviation_moved = moved_operations.groupby('Workcenter')['Difference'].min().reset_index(name='min_deviation_moved')

# Step 2: Calculate the number of operations with no change (Difference == 0)
no_change_count = df[df['Difference'] == 0].groupby('Workcenter').size().reset_index(name='num_no_change')

# Step 3: Calculate the number of operations that did change (Difference != 0)
changed_count = df[df['Difference'] != 0].groupby('Workcenter').size().reset_index(name='num_changed')

# Step 4: Merge all calculated data into a single DataFrame
summary_df = avg_deviation_moved.merge(max_deviation_moved, on='Workcenter', how='outer')
summary_df = summary_df.merge(min_deviation_moved, on='Workcenter', how='outer')
summary_df = summary_df.merge(no_change_count, on='Workcenter', how='left')
summary_df = summary_df.merge(changed_count, on='Workcenter', how='left')

# Fill NaN values in num_no_change and num_changed with 0
summary_df['num_no_change'] = summary_df['num_no_change'].fillna(0)
summary_df['num_changed'] = summary_df['num_changed'].fillna(0)

# Step 5: Sort the work centers in a specific order (e.g., 400A, 400B, 401, etc.)
workcenter_order = ['400A', '400B', '401', '402', '403', '404', '405', '406', '407', '408', '409', '4010', 
                    '4011', '4012', '4013', '4014', '4015', '4016', '4017']

summary_df['Workcenter'] = pd.Categorical(summary_df['Workcenter'], categories=workcenter_order, ordered=True)
summary_df = summary_df.sort_values('Workcenter')

# Step 6: Create a grouped bar chart showing average deviation, number of no-change operations, and number of changed operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='Workcenter', 
    y=['avg_deviation_moved', 'num_no_change', 'num_changed'],  # Show metrics for deviation and operations
    title="Impact of Deviations by Workcenter (Only Moved Operations Included in Avg. Deviation)",
    labels={'avg_deviation_moved': 'Average Deviation (Moved Operations)', 'num_no_change': 'No Change (Count)', 'num_changed': 'Changed Operations (Count)'},
    barmode='group',  # Group bars for better comparison
    height=600,
    width=1000
)

# Step 7: Add annotations to the bars for better readability
for bar in fig_grouped_bar.data:
    bar.text = bar.y
    bar.textposition = 'outside'

# Step 8: Set a consistent y-axis range for all bars to keep the same scale
fig_grouped_bar.update_layout(
    xaxis_title="Planned Workcenter",
    yaxis_title="Deviation / Operation Count",
    showlegend=True,
    legend_title_text="Metrics",
    uniformtext_minsize=8, 
    uniformtext_mode='hide',
    yaxis=dict(range=[0, max(summary_df[['avg_deviation_moved', 'num_no_change', 'num_changed']].max().max()) * 1.1])  # Scale the y-axis
)

# Display the figure
fig_grouped_bar.show()