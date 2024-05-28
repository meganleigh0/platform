import plotly.graph_objects as go
import pandas as pd


# Generate distinct colors for each variant
num_variants = 13  # You mentioned having 13 different variants
colors = px.colors.qualitative.Alphabet  # Use Plotly's Alphabet color scale, which has enough unique colors

# Ensure there are enough colors by repeating the color list if necessary
if len(colors) < num_variants:
    colors = colors * (num_variants // len(colors) + 1)

# Create a Sankey diagram for each family
for family, variants in mbom_pipelines.items():
    all_data = pd.DataFrame()
    variant_labels = []

    # Combine data from all variants
    for i, (variant, data) in enumerate(variants.items()):
        data['Variant'] = variant  # Tag each row with its variant
        all_data = pd.concat([all_data, data])
        if variant not in variant_labels:
            variant_labels.append(variant)

    # Group data to summarize flows
    sankey_data = all_data.groupby(['Facility', 'Source', 'Variant'])['Qty'].sum().reset_index()

    # Map labels to unique IDs
    labels = pd.concat([sankey_data['Facility'], sankey_data['Source']]).unique()
    label_dict = {label: i for i, label in enumerate(labels)}

    # Apply mappings to create source and target IDs
    sankey_data['SourceID'] = sankey_data['Facility'].map(label_dict)
    sankey_data['TargetID'] = sankey_data['Source'].map(label_dict)

    # Node data
    node_trace = go.sankey.Node(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=['rgba(211,211,211,0.5)' for _ in labels]  # Light gray color for nodes
    )

    # Link data (for flows between nodes)
    link_trace = go.sankey.Link(
        source=sankey_data['SourceID'],
        target=sankey_data['TargetID'],
        value=sankey_data['Qty'],
        color=[colors[variant_labels.index(var)] for var in sankey_data['Variant']]  # Color links by variant
    )

    # Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=node_trace,
        link=link_trace,
        arrangement='snap'
    )])

    fig.update_layout(title_text=f"Material Flow Sankey Diagram for {family}", font_size=10)
    fig.show()





import pandas as pd

def calculate_daily_headcount(dept_logger, num_months):
    main_df = pd.DataFrame(dept_logger.log)
    daily_heads = []
    heads_list = {}
    end = num_months * 160  # Calculate the end based on number of months and hours per month

    for k in range(int(end // 8)):
        heads_list[f'{k}'] = {}
        period_df = main_df[(main_df['Timestamp'] < 8*(k+1)) & (main_df['Timestamp'] > 8*k)]

        for _, row in period_df.iterrows():
            department = row['Department']
            interaction = row['Interaction']
            if department not in heads_list[f'{k}']:
                heads_list[f'{k}'][department] = [interaction]
            else:
                heads_list[f'{k}'][department].append(interaction)

        daily_headcount = 0
        for department in heads_list[f'{k}'].keys():
            unique_heads = set(heads_list[f'{k}'][department])
            headcount = 8 * len(unique_heads)  # Multiply by hours in a day to get man-hours
            heads_list[f'{k}'][department] = headcount
            daily_headcount += headcount
        
        daily_heads.append(daily_headcount)

    return daily_heads

# Example Usage
dept_logger = pd.DataFrame()  # Replace with actual DataFrame loading
num_months = 20
daily_headcounts = calculate_daily_headcount(dept_logger, num_months)

