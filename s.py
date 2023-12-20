import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd

def create_utilization_dashboard(df):
    """
    Create a dashboard showing plant and department utilization.

    Parameters:
    df (DataFrame): A DataFrame containing columns - Department, DepartmentID, Plant, Timestamp, Utilization

    Returns:
    go.Figure: A Plotly figure object containing the visualization.
    """

    # Convert utilization to percentage for easier interpretation
    df['Utilization'] = df['Utilization'] * 100

    # Aggregate utilization by plant to get an average utilization for each plant
    plant_utilization = df.groupby('plant')['Utilization'].mean().reset_index()

    # Number of unique plants determines the number of columns in the subplot
    num_plants = len(plant_utilization['plant'].unique())

    # Create a subplot with two rows: one for plant gauges and one for department bar charts
    fig = sp.make_subplots(
        rows=2, cols=num_plants,
        subplot_titles=[f"Plant {plant}" for plant in plant_utilization['plant'].unique()] + [None] * num_plants,
        specs=[[{"type": "indicator"}] * num_plants, [{"type": "bar"}] * num_plants]
    )

    # Add gauge and bar charts for each plant
    for i, plant in enumerate(plant_utilization['plant'].unique(), 1):
        # Gauge chart for overall plant utilization
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=plant_utilization[plant_utilization['plant'] == plant]['Utilization'].iloc[0],
                title={'text': f"Plant {plant} Utilization"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
            ),
            row=1, col=i
        )

        # Bar chart for detailed department utilization within the plant
        department_utilization = df[df['plant'] == plant].groupby('Department')['Utilization'].mean().reset_index()
        fig.add_trace(
            go.Bar(
                x=department_utilization['Department'],
                y=department_utilization['Utilization'],
                name=f"Dept Utilization in {plant}"
            ),
            row=2, col=i
        )

    # Update layout for better presentation
    fig.update_layout(
        title_text="Plant and Department Utilization Overview",
        height=600,
        showlegend=False
    )

    return fig

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# fig = create_utilization_dashboard(df)
# fig.show()
