import plotly.graph_objects as go

source = [index for OrgA, OrgB, ...]  # indices of source nodes
target = [index for Src1, Src2, ...]  # indices of target nodes
value = [count of parts]  # values for each link

label = ["OrgA", "OrgB", ..., "Src1", "Src2", ...]  # labels for nodes

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=label
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    ))])

fig.update_layout(title_text="Flow of parts from Usr Org to Src Org by Make/Buy status")
fig.show()