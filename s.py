import pandas as pd
import plotly.graph_objects as go

# Example DataFrame
data = {
    'mbomID': [1, 2, 3],
    'ParentID': [0, 1, 1],
    'PartNumber': ['100', '101', '102'],
    'Description': ['Assembly', 'Part A', 'Part B'],
    'Qty': [100, 200, 150],
    'Make/Buy': ['Make', 'Buy', 'Make'],
    'Children': [['101', '102'], [], []],
    'Descendants': [['101', '102'], [], []],
    'Facility': ['Main Plant', 'Feeder Plant 1', 'Main Plant'],
    'Source': ['Main Plant', 'Main Plant', 'Feeder Plant 1']
}

df = pd.DataFrame(data)

# Adjusting data to avoid self loops where not meaningful
# Filtering out rows where Facility and Source are the same
df = df[df['Facility'] != df['Source']]

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
    pad=15,  # Padding between nodes
    thickness=20,  # Node thickness
    line=dict(color="black", width=0.5),  # Border line
    label=labels,
    color="blue"
)

# Link data (for flows between nodes)
link_trace = go.sankey.Link(
    source=sankey_data['SourceID'], 
    target=sankey_data['TargetID'], 
    value=sankey_data['Qty']
)

# Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=node_trace,
    link=link_trace,
    arrangement='snap')])

fig.update_layout(title_text="Improved Material Flow Sankey Diagram", font_size=10)
fig.show()
