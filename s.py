
# Create a Sankey diagram for each family
for family, variants in mbom_pipelines.items():
    all_data = pd.DataFrame()
    variant_labels = []

    # Combine data from all variants
    for i, (variant, data) in enumerate(variants.items()):
        data['Variant'] = variant  # Tag each row with its variant
        all_data = pd.concat([all_data, data])
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
        color=[variant_colors[variant_labels.index(var)] for var in sankey_data['Variant']]  # Color links by variant
    )

    # Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=node_trace,
        link=link_trace,
        arrangement='snap'
    )])

    fig.update_layout(title_text=f"Material Flow Sankey Diagram for {family}", font_size=10)
    fig.show()
