# Create a Sankey diagram for each Usr Org
sankey_data = []

for usr_org in df['Usr Org'].unique():
    # Filter data for the current Usr Org
    filtered_df = df[df['Usr Org'] == usr_org]

    # Count parts from each Src Org for the current Usr Org
    count_by_src = filtered_df.groupby('Src Org').size().reset_index(name='Count')

    # Create data for the Sankey diagram
    source = [0] * len(count_by_src)  # Source is always the Usr Org in this case
    target = [1 + i for i in range(len(count_by_src))]  # Targets are the Src Orgs
    value = count_by_src['Count'].tolist()
    label = [usr_org] + count_by_src['Src Org'].tolist()

    sankey_data.append({
        'usr_org': usr_org,
        'source': source,
        'target': target,
        'value': value,
        'label': label
    })

# Display an example of what the data looks like for the first Usr Org
sankey_data[0]