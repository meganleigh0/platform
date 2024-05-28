# Create a Sankey diagram for each family and variant
for family, variants in mbom_pipelines.items():
    for variant, data in variants.items():
        df = data

        # Group data to summarize flows
        sankey_data = df.groupby(['Facility', 'Source'])['Qty'].sum().reset_index()

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
            color=[variant_colors[variant] if x % 2 == 0 else flow_direction_colors['incoming'] for x in range(len(labels))]
        )

        # Link data (for flows between nodes)
        link_trace = go.sankey.Link(
            source=sankey_data['SourceID'],
            target=sankey_data['TargetID'],
            value=sankey_data['Qty'],
            color=[flow_direction_colors['outgoing'] if i % 2 == 0 else variant_colors[variant] for i in range(len(sankey_data))]
        )

        # Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=node_trace,
            link=link_trace,
            arrangement='snap'
        )])

        fig.update_layout(title_text=f"Material Flow Sankey Diagram for {family} - {variant}", font_size=10)
        fig.show()
