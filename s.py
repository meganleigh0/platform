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
            interactions = row['Interaction']
            if department not in period_heads:
                period_heads[department] = set()
            # Assume interactions is a list of hashable items
            period_heads[department].update(interactions)  # Add all interactions to the set

        for department in period_heads:
            headcount = 8 * len(period_heads[department])  # Calculate man-hours for unique interactions
            daily_headcount += headcount

        daily_heads.append(daily_headcount)

    return daily_heads

# Example Usage
dept_logger = pd.DataFrame()  # Replace with actual DataFrame loading
num_months = 20
daily_headcounts = calculate_daily_headcount(dept_logger, num_months)



# Define color scales for each family
family_colors = {
    'Family1': px.colors.sequential.Blues,
    'Family2': px.colors.sequential.Greens
}

# Function to create Sankey diagram for each family
def create_sankey_for_family(family, data):
    fig = go.Figure()

    # Create traces for each variant
    for i, (variant, df) in enumerate(data.items()):
        sankey_data = df.groupby(['Facility', 'Source'])['Qty'].sum().reset_index()
        labels = pd.concat([sankey_data['Facility'], sankey_data['Source']]).unique()
        label_dict = {label: idx for idx, label in enumerate(labels)}
        sankey_data['SourceID'] = sankey_data['Facility'].map(label_dict)
        sankey_data['TargetID'] = sankey_data['Source'].map(label_dict)

        nodes = go.sankey.Node(
            pad=15, thickness=20, line=dict(color='black', width=0.5),
            label=labels, color=family_colors[family][:len(labels)]
        )
        links = go.sankey.Link(
            source=sankey_data['SourceID'], target=sankey_data['TargetID'], value=sankey_data['Qty'],
            color=family_colors[family][len(labels):len(labels)+len(sankey_data)]
        )
        sankey = go.Sankey(node=nodes, link=links)
        fig.add_trace(sankey)

    # Dropdown for variants
    buttons = []
    for i, variant in enumerate(data):
        button = dict(
            label=variant,
            method="update",
            args=[{"visible": [False] * len(data)},  # Hide all traces
                  {"title": f"{family} - {variant}"}]
        )
        button["args"][0]["visible"][i] = True  # Show current variant
        buttons.append(button)

    # Add dropdown
    fig.update_layout(
        updatemenus=[{
            "x": 0.1,
            "y": 1.15,
            "xanchor": 'left',
            "yanchor": 'top',
            "buttons": buttons
        }],
        title_text=f"Material Flow Sankey Diagram for {family}"
    )

    return fig

# Generate plots for each family
for family, variants in mbom_pipelines.items():
    fig = create_sankey_for_family(family, variants)
    fig.show()
