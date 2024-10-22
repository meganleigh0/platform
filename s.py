import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Sample data preparation
data = {
    'Program': ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C'],
    'Operator': ['Op1', 'Op2', 'Op1', 'Op3', 'Op2', 'Op1', 'Op3', 'Op4', 'Op2'],
    'WCAssigned': ['WC1', 'WC2', 'WC1', 'WC2', 'WC3', 'WC1', 'WC2', 'WC3', 'WC1'],
    'Hours': [5, 3, 8, 2, 7, 4, 6, 3, 5],
    'Criticality Rating': [1, 2, 1, 2, 1, 2, 1, 1, 2]
}
all_dfs = pd.DataFrame(data)

# Aggregation for total hours by program
hours_by_program = all_dfs.groupby('Program')['Hours'].sum().reset_index()

# Aggregation for total hours by work center within each program
hours_by_wc_program = all_dfs.groupby(['Program', 'WCAssigned'])['Hours'].sum().reset_index()

# Creating a figure with subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Total Hours by Program', 'Total Hours by Work Center per Program'),
    specs=[[{"type": "bar"}, {"type": "bar"}]]
)

# Total Hours by Program
fig.add_trace(
    go.Bar(x=hours_by_program['Program'], y=hours_by_program['Hours'], text=hours_by_program['Hours'], 
           textposition='auto', marker_color='indianred'),
    row=1, col=1
)

# Total Hours by Work Center per Program - Each program's bar chart
programs = hours_by_wc_program['Program'].unique()
colors = ['lightslategray', 'lightseagreen', 'indianred']  # Adjust color for visual distinction

for idx, program in enumerate(programs):
    df_filtered = hours_by_wc_program[hours_by_wc_program['Program'] == program]
    fig.add_trace(
        go.Bar(x=df_filtered['WCAssigned'], y=df_filtered['Hours'], text=df_filtered['Hours'],
               textposition='auto', name=f'Program {program}', marker_color=colors[idx % len(colors)]),
        row=1, col=2
    )

# Update layout for clear visualization
fig.update_layout(
    title_text='Operations Distribution Overview',
    barmode='group',
    showlegend=True
)

# Show the plot
fig.show()
