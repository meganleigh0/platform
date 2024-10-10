import plotly.express as px
import pandas as pd

# Group data by Workcenter to summarize the deviation statistics
summary_df = df.groupby('Workcenter').agg(
    avg_deviation=('Difference', 'mean'),
    max_deviation=('Difference', 'max'),
    min_deviation=('Difference', 'min'),
    total_ops=('Difference', 'size')
).reset_index()

# Calculate the number of operations with no change (Difference = 0)
summary_df['num_no_change'] = df.groupby('Workcenter')['Difference'].apply(lambda x: (x == 0).sum()).values

# Create a grouped bar chart showing average deviation and number of no-change operations per work center
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