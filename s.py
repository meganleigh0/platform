import pandas as pd
import plotly.express as px

def veh_graphs():
    # Load your data
    df = pd.read_csv('logs/assembly.csv')

    # Calculate duration for the scatter plot
    df['Duration'] = round(df['Timestamp_end'] - df['Timestamp_start'], 2)
    station_count = df['Station'].value_counts()

    # Create station bar chart with updated y-axis label and title
    station_bar_chart = px.bar(station_count, labels={'index': 'Station', 'value': 'Assembly Count'})
    station_bar_chart.update_layout(title='Station Assembly Count', yaxis_title='Assembly Count')

    # Create assembly duration scatter plot with title
    assembly_duration_scatter_plot = px.scatter(df, x='Station', y='Duration', color='Assembly')
    assembly_duration_scatter_plot.update_layout(title='Assembly Duration per Station')

    # Create workflow time series line chart with title
    workflow_time_series = px.line(df, x='Timestamp_start', y='Assembly')
    workflow_time_series.update_layout(title='Workflow Time Series')

    return station_bar_chart, assembly_duration_scatter_plot, workflow_time_series
