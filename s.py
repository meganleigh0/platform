import pandas as pd

# Assuming vehicle_a_mboms and vehicle_s_mboms are your dictionaries containing the MBOM dataframes

def prepare_sankey_data(mboms):
    data = []
    for variant, df in mboms.items():
        for index, row in df.iterrows():
            data.append({
                'source': row['Src Org'],
                'target': row['Usr Org'],
                'value': row['Qty'],
                'variant': variant
            })
    return data

data_a = prepare_sankey_data(vehicle_a_mboms)
data_s = prepare_sankey_data(vehicle_s_mboms)

# Combine data from both vehicles
sankey_data = data_a + data_s

def get_nodes_links(data):
    unique_orgs = set()
    for item in data:
        unique_orgs.update([item['source'], item['target']])
    
    nodes = list(unique_orgs)
    links = {
        'source': [],
        'target': [],
        'value': [],
        'color': [],  # Optional, to color by variant
    }
    
    node_indices = {node: i for i, node in enumerate(nodes)}
    for item in data:
        links['source'].append(node_indices[item['source']])
        links['target'].append(node_indices[item['target']])
        links['value'].append(item['value'])
        links['color'].append(item['variant'])  # This will be used to map colors to variants
    
    return nodes, links

nodes, links = get_nodes_links(sankey_data)

import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color='blue'  # Default color, modify as needed
    ),
    link=dict(
        source=links['source'],  # indices correspond to labels, eg A1, A2, A2, B1, ...
        target=links['target'],
        value=links['value'],
        color=links['color']  # Optional, to color by variant
    ))])

fig.update_layout(title_text="Sankey Diagram for Vehicle Parts Flow", font_size=10)
fig.show()
