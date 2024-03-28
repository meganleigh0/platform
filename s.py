import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Sample structure of mbom_dfs
# mbom_dfs = {
#     'variant1': pd.DataFrame({
#         'PartNumber': [...],
#         'Description': [...],
#         'mbomID': [...],
#         'ParentID': [...],
#         'make/buy': [...],
#         'Number of Children': [...],
#         'Src Org': [...],
#         'Usr Org': [...]
#     }),
#     ...
# }

# Initialize lists for Sankey diagram data
flows = []
labels = []
label_indices = {}

# Loop through each product variant in the dictionary
for variant, df in mbom_dfs.items():
    # Loop through each row in the dataframe
    for _, row in df.iterrows():
        src = row['Src Org']
        usr = row['Usr Org']
        flow = 1  # Or use another column or calculation for the flow magnitude

        # Add source and user orgs to labels if they are not already there
        for org in [src, usr]:
            if org not in label_indices:
                label_indices[org] = len(labels)
                labels.append(org)

        # Add the flow between the source and user orgs
        flows.append((label_indices[src], label_indices[usr], flow))

# Generate the Sankey diagram
sankey = Sankey()

# Since we have the indices for each org in label_indices, we can directly use flows
# orientations is not needed unless you want to specify the direction of each individual flow
sankey.add(flows=flows, labels=labels)

# Draw the Sankey diagram
sankey.finish()
plt.show()
