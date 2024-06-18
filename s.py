import pandas as pd
import plotly.express as px

# Example DataFrame creation (you will replace this with your actual DataFrame)
data = {
    'Program': ['A', 'B', 'C'],
    'JAN_2022': [100, 150, 200],
    'FEB_2022': [120, 160, 210],
    # Add all your other columns here
}
df = pd.DataFrame(data)
df.set_index('Program', inplace=True)

# Transform DataFrame for Plotly
df_long = df.stack().reset_index()
df_long.columns = ['Program', 'Date', 'Vehicles']
df_long['Year'] = df_long['Date'].apply(lambda x: x.split('_')[1])
df_long['Month'] = df_long['Date'].apply(lambda x: x.split('_')[0])

# Create a Heatmap
fig = px.density_heatmap(df_long, x='Month', y='Year', z='Vehicles', facet_col='Program', color_continuous_scale='Viridis')
fig.show()