# Map Facility and Source to numeric IDs
label_list = pd.concat([sankey_data['Facility'], sankey_data['Source']]).unique()
label_dict = {label: idx for idx, label in enumerate(label_list)}

# Map the labels to integers for Plotly
sankey_data['SourceID'] = sankey_data['Facility'].map(label_dict)
sankey_data['TargetID'] = sankey_data['Source'].map(label_dict)

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=label_list,
        color="blue"
    ),
    link=dict(
        source=sankey_data['SourceID'],
        target=sankey_data['TargetID'],
        value=sankey_data['Qty']
    ))])

fig.update_layout(title_text="Material Flow Sankey Diagram", font_size=10)
