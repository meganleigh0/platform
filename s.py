import pandas as pd
import plotly.express as px

# Step 1: Group by Workcenter and calculate the basic statistics
workcenter_stats = df.groupby('Workcenter').agg(
    avg_deviation=('Difference', 'mean'),
    max_deviation=('Difference', 'max'),
    min_deviation=('Difference', 'min'),
    total_ops=('Difference', 'size')
).reset_index()

# Step 2: Calculate the number of operations with no changes (Difference == 0)
no_change_count = df[df['Difference'] == 0].groupby('Workcenter').size().reset_index(name='num_no_change')

# Step 3: Merge the two DataFrames
summary_df = pd.merge(workcenter_stats, no_change_count, on='Workcenter', how='left')

# Step 4: Fill NaN values in num_no_change with 0 (in case there were no operations with 0 difference for some workcenters)
summary_df['num_no_change'] = summary_df['num_no_change'].fillna(0)

# Step 5: Create a grouped bar chart showing average deviation and number of no-change operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='Workcenter', 
    y=['avg_deviation', 'num_no_change'],  # Show both deviation and