# Initialize a directed graph
G = nx.DiGraph()

# Add nodes and edges
for idx, row in df.iterrows():
    G.add_node(row['Facility'], color='cyan', size=row['Qty']*100)
    G.add_node(row['Source'], color='lightblue', size=row['Qty']*100)
    G.add_edge(row['Facility'], row['Source'], weight=row['Qty'])

# Drawing the graph
pos = nx.spring_layout(G, seed=42)  # positions for all nodes

sizes = [G.nodes[node]['size'] for node in G.nodes]
colors = [G.nodes[node]['color'] for node in G.nodes]

# nodes
nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, alpha=0.6)

# edges
edges = nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# labels
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

plt.title("Network Graph of MBOM Flow")
plt.axis('off')  # Turn off the axis
plt.show()
