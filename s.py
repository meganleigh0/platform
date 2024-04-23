import pandas as pd
import plotly.graph_objects as go

# Aggregate data to get counts from Src Org to Usr Org
flow_counts = mbom.groupby(['Src Org', 'Usr Org']).size().reset_index(name='Count')

# Create lists of unique orgs for labeling
all_orgs = pd.concat([flow_counts['Src Org'], flow_counts['Usr Org']]).unique()

# Create a mapping from org names to indices
org_index = {org: i for i, org in enumerate(all_orgs)}

# Map the org names in Src Org and Us Org to their respective indices
flow_counts['Source'] = flow_counts['Src Org'].map(org_index)
flow_counts['Target'] = flow_counts['Usr Org'].map(org_index)
flow_counts['Value'] = flow_counts['Count']

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=50,
        thickness=10,  # Adjust thickness here
        line=dict(color="black", width=0.5),  # Adjust line color and width here
        label=all_orgs,
    ),
    link=dict(
        source=flow_counts['Source'],
        target=flow_counts['Target'],
        value=flow_counts['Value'],
        color="blue",  # Adjust link color here
    )
)])

# Update layout with customizations
fig.update_layout(
    title_text="Flow of Parts Between Organizations",
    font_size=12,  # Adjust font size here
)
fig.show()