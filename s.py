import pandas as pd

# Load the data from the CSV file
mbom = pd.read_csv('mbom.csv')

# Display the first few rows of the dataframe to understand its structure
print(mbom.head())

# Count the number of parts used at each Usr Org
usage_count = mbom['Usr Org'].value_counts()
print("\nNumber of parts used at each Usr Org:")
print(usage_count)

# Count the number of parts from each Src Org for each Usr Org
source_usage_count = mbom.groupby(['Src Org', 'Usr Org']).size().unstack(fill_value=0)
print("\nNumber of parts from each Src Org for each Usr Org:")
print(source_usage_count)

import pandas as pd
import plotly.graph_objects as go

# Load the data
mbom = pd.read_csv('mbom.csv')

# Aggregate data to get counts from Src Org to Usr Org
flow_counts = mbom.groupby(['Src Org', 'Usr Org']).size().reset_index(name='Count')

# Create lists of unique orgs for labeling
all_orgs = pd.concat([flow_counts['Src Org'], flow_counts['Usr Org']]).unique()

# Create a mapping from org names to indices
org_index = {org: i for i, org in enumerate(all_orgs)}

# Map the org names in Src Org and Usr Org to their respective indices
flow_counts['Source'] = flow_counts['Src Org'].map(org_index)
flow_counts['Target'] = flow_counts['Usr Org'].map(org_index)
flow_counts['Value'] = flow_counts['Count']

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
      pad=15,
      thickness=20,
      line=dict(color="black", width=0.5),
      label=all_orgs
    ),
    link=dict(
      source=flow_counts['Source'],
      target=flow_counts['Target'],
      value=flow_counts['Value']
    ))])

fig.update_layout(title_text="Flow of Parts Between Organizations", font_size=10)
fig.show()
