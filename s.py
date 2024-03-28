import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Assuming mbom_dfs is your provided dictionary with dataframes
# For example:
# mbom_dfs = {
#     'variant1': pd.DataFrame({
#         'PartNumber': [..],
#         'Description': [..],
#         'mbomID': [..],
#         'ParentID': [..],
#         'make/buy': [..],
#         'Number of Children': [..],
#         'Src Org': [..],
#         'Usr Org': [..]
#     }),
#     ...
# }

flows = []
labels = []
label_indices = {}

for variant, df in mbom_dfs.items():
    for _, row in df.iterrows():
        src = row['Src Org']
        usr = row['Usr Org']
        flow = 1  # Or determine the flow based on your data specifics

        # Assign unique indices to each organization
        for org in [src, usr]:
            if org not in label_indices:
                label_indices[org] = len(labels)
                labels.append(org)

        flows.append((label_indices[src], label_indices[usr], flow))

# Preparing the Sankey diagram data
sankey_flows = []
sankey_labels = []
for src, dst, flow in flows:
    sankey_flows.append((src, dst, flow))
    sankey_labels.append(labels[src])  # add source label
    sankey_labels.append(labels[dst])  # add destination label

# Draw the Sankey diagram
sankey = Sankey()

# Add flows to the Sankey diagram
# Ensure each flow has a corresponding orientation, which can be 0 (left or right)
orientations = [0] * len(sankey_flows)  # For simplicity, assuming all flows are left-to-right or right-to-left
sankey.add(flows=sankey_flows, labels=sankey_labels, orientations=orientations)

# Finish and show the Sankey diagram
sankey.finish()
plt.show()
