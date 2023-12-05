import pandas as pd
import plotly.express as px

# Assuming 'df' is your DataFrame with the simulation data
# Example: df = pd.read_csv('your_data.csv')

data = {
    "Interaction": [
        "Divorce Structure 1", "Start Plant 1 Hull 1", "Start Plant 1 Turret 1",
        "Divorce Structure 2", "Start Plant 1 Hull 2", "Start Plant 1 Turret 2",
        "Complete Plant 1 Hull 1", "Hull Status", "Turret Status"
    ],
    "Timestamp": [
        0.000, 4.060, 4.060,
        0.000, 4.060, 4.060,
        16.060, 17.000, 17.000
    ],
    "Completed": [None, None, None, None, None, None, None, 1, 1],
    "InProcessing": [None, None, None, None, None, None, None, 1, 1]
}

df = pd.DataFrame(data)
# Gantt Chart for Timeline Events
import pandas as pd
import plotly.express as px

# Assuming 'df' is your DataFrame
# Example: df = pd.read_csv('your_data.csv')

# Pivoting the DataFrame for suitable format
df_pivot = df.pivot_table(index='Timestamp', columns='Interaction', values=['InProcessing', 'Completed'], fill_value=0)

# Resetting index to get 'Timestamp' as a column
df_pivot.reset_index(inplace=True)

# Melting the DataFrame for Plotly
df_melted = df_pivot.melt(id_vars=['Timestamp'], var_name='Process', value_name='Count')

# Creating the animated bar chart
fig = px.bar(df_melted, x='Process', y='Count', color='Process', animation_frame='Timestamp')

# Customizing the layout
fig.update_layout(title='Simulation Process Over Time', xaxis_title='Process', yaxis_title='Count')

# Showing the plot
fig.show()


import plotly.express as px

# Assuming df_melted is your prepared DataFrame
fig = px.bar(df_melted, x='Process', y='Count', color='Process', animation_frame='Timestamp')

# Update layout for animation speed and transition duration
fig.update_layout(
    title='Simulation Process Over Time',
    xaxis_title='Process',
    yaxis_title='Count',
    # Adjusting animation frame duration (in milliseconds)
    updatemenus=[{
        'buttons': [{
            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'linear'}}],
            'label': 'Play',
            'method': 'animate'
        }]
    }]
)

# Showing the plot
fig.show()

