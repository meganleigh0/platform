import plotly.express as px
import pandas as pd

# Group data by WorkCenter to summarize the deviation statistics
summary_df = df.groupby('WorkCenter').agg(
    avg_deviation=('Difference', 'mean'),
    max_deviation=('Difference', 'max'),
    min_deviation=('Difference', 'min'),
    total_ops=('Difference', 'size'),
    num_no_change=('Difference', lambda x: sum(x == 0))  # Count operations with no change
).reset_index()

# Create a grouped bar chart showing average deviation and number of no-change operations per work center
fig_grouped_bar = px.bar(
    summary_df, 
    x='WorkCenter', 
    y=['avg_deviation', 'num_no_change'],  # Show both deviation and stability metrics
    title="Impact of Deviations by WorkCenter",
    labels={'avg_deviation': 'Average Deviation', 'num_no_change': 'No Change (Count)'},
    barmode='group',  # Group bars for better comparison
    height=600,
    width=1000
)

fig_grouped_bar.update_layout(
    xaxis_title="Planned WorkCenter",
    yaxis_title="Deviation / No Change Count",
    showlegend=True,
    legend_title_text="Metrics"
)

fig_grouped_bar.show()