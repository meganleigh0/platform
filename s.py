import pandas as pd

def calculate_daily_headcount(dept_logger, num_months):
    main_df = pd.DataFrame(dept_logger.log)
    daily_heads = []
    end = num_months * 160  # Calculate the end based on number of months and hours per month

    for k in range(int(end // 8)):
        daily_headcount = 0
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]
        period_heads = {}

        for _, row in period_df.iterrows():
            department = row['Department']
            interaction = row['Interaction']
            if department not in period_heads:
                period_heads[department] = set()  # Use a set to store unique interactions
            period_heads[department].add(interaction)  # Add interaction directly to the set

        for department in period_heads:
            headcount = 8 * len(period_heads[department])  # Calculate man-hours for unique interactions
            daily_headcount += headcount

        daily_heads.append(daily_headcount)

    return daily_heads

# Example Usage
dept_logger = pd.DataFrame()  # Replace with actual DataFrame loading
num_months = 20
daily_headcounts = calculate_daily_headcount(dept_logger, num_months)


import plotly.graph_objects as go
import pandas as pd

# Example data
mbom_pipelines = {
    'Family1': {
        'Variant1': pd.DataFrame({'Facility': ['A', 'B'], 'Source': ['B', 'C'], 'Qty': [100, 150]}),
        'Variant2': pd.DataFrame({'Facility': ['A', 'B'], 'Source': ['B', 'C'], 'Qty': [200, 250]}),
        # Assume more variants as needed
    }
}

# Define colors for each variant
colors = [
    'blue', 'green', 'red', 'purple', 'orange', 'yellow', 'cyan', 'magenta',
    'lime', 'pink', 'teal', 'lavender', 'olive'
]

# Create a Sankey diagram for each family with a dropdown to filter by variant
for family, variants in mbom_pipelines.items():
    fig = go.Figure()

    variant_labels = list(variants.keys())
    max_variants = len(variant_labels)

    # Ensure enough colors
    if len(colors) < max_variants:
        colors = colors * (max_variants // len(colors) + 1)

    steps = []

    # Create a Sankey diagram for each variant
    for i, (variant, data) in enumerate(variants.items()):
        sankey_data = data.groupby(['Facility', 'Source'])['Qty'].sum().reset_index()
        labels = pd.concat([sankey_data['Facility'], sankey_data['Source']]).unique()
        label_dict = {label: idx for idx, label in enumerate(labels)}
        sankey_data['SourceID'] = sankey_data['Facility'].map(label_dict)
        sankey_data['TargetID'] = sankey_data['Source'].map(label_dict)

        # Nodes and Links
        nodes = go.sankey.Node(
            pad=15, thickness=20, line=dict(color='black', width=0.5),
            label=labels, color='grey'
        )
        links = go.sankey.Link(
            source=sankey_data['SourceID'], target=sankey_data['TargetID'], value=sankey_data['Qty'],
            color=colors[i]
        )
        sankey = go.Sankey(node=nodes, link=links)

        # Only show the current variant in the dropdown
        step = dict(
            method="update",
            args=[{"visible": [False] * max_variants},  # Hide all traces
                  {"title": f"Material Flow for {family} - {variant}"}],
            label=variant
        )
        step["args"][0]["visible"][i] = True  # Toggle i-th trace to "visible"
        steps.append(step)

        fig.add_trace(sankey)

    # Add dropdown
    fig.update_layout(
        updatemenus=[{
            "x": 0.1,
            "y": 1.1,
            "xanchor": 'left',
            "yanchor": 'top',
            "buttons": steps
        }],
        title_text=f"Material Flow Sankey Diagram for {family}"
    )

    fig.show()
