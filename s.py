for variant, df in lim_dfs.items():
    print(f"Variant: {variant}")
    print("DataFrame Summary:")
    print(df.describe())  # Summarize the DataFrame, showing stats for numerical columns
    print("\nFirst 5 Rows:")
    print(df.head())  # Show the first 5 rows to get a sense of the data
    print("\nStation Assignments Distribution:")
    print(df['Station'].value_counts())  # Show distribution of station assignments
    print("\nOperations Mapping Sample:")
    print(df[['mbomID', 'Operations']].head())  # Sample operations mapping for the first 5 rows
    print("-" * 50)

def print_tree_info(node, level=0):
    indent = "  " * level  # Indentation to visualize tree structure
    print(f"{indent}Node: {node.mbomID}, Station: {node.station}, Operations: {node.operations}")
    for child in node.children:
        print_tree_info(child, level + 1)  # Recursive call to print child info
for variant, root_node in lim_trees.items():
    print(f"Inspecting tree for variant: {variant}")
    print_tree_info(root_node)
    print("-" * 50)
