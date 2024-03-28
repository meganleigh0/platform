import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.sankey import Sankey

# Assuming mbom_dfs is a dictionary with keys as product variants and values as dataframes
# mbom_dfs = {
#     'variant1': df1,
#     'variant2': df2,
#     ...
# }

# Prepare a list to collect the flow data
flows = []

# Iterate through each product variant's dataframe
for variant, df in mbom_dfs.items():
    # For each part, summarize the flow from Src Org to Usr Org
    for index, row in df.iterrows():
        src_org = row['Src Org']
        usr_org = row['Usr Org']
        flow_value = 1  # Or some other logic to determine the quantity or importance of the flow

        # Add the flow to the list
        flows.append((src_org, usr_org, flow_value))

# Aggregate flows between the same Src Org and Usr Org
flow_data = pd.DataFrame(flows, columns=['Src Org', 'Usr Org', 'Flow'])
aggregate_flows = flow_data.groupby(['Src Org', 'Usr Org']).sum().reset_index()

# Now aggregate_flows contains the summarized flow data between organizations
# Next, we can use this data to create a Sankey diagram

# Prepare data for the Sankey diagram
sankey_flows = []
sankey_labels = []
label_mapping = {}

for index, row in aggregate_flows.iterrows():
    src_org, usr_org, flow = row['Src Org'], row['Usr Org'], row['Flow']

    # Check if we already have the src_org in the labels list
    if src_org not in label_mapping:
        label_mapping[src_org] = len(sankey_labels)
        sankey_labels.append(src_org)

    # Check if we already have the usr_org in the labels list
    if usr_org not in label_mapping:
        label_mapping[usr_org] = len(sankey_labels)
        sankey_labels.append(usr_org)

    # Add the flow (negative for source, positive for user)
    sankey_flows.append((label_mapping[src_org], label_mapping[usr_org], flow))

# Plot the Sankey diagram
sankey = Sankey()

# Add flows to the Sankey diagram
for src, dst, flow in sankey_flows:
    sankey.add(flows=[(src, dst, flow)], labels=sankey_labels, orientations=[-1, 1])

# Draw the Sankey diagram
sankey.finish()
plt.show()
