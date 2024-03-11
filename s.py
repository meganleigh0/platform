import altair as alt

# Assuming all_operations is already loaded into a DataFrame

# Define bins for the Hours
bin_edges = [0, 10, 20, 100, max(all_operations['Hours'])]  # Assuming this covers all possible hours
bin_labels = ['1-10 Hours', '11-20 Hours', '21-100 Hours', '100+ Hours']

# Assign each operation to a bin
all_operations['HourBin'] = pd.cut(all_operations['Hours'], bins=bin_edges, labels=bin_labels, right=False)

# Now, create a bubble chart with customized sizes
chart = alt.Chart(all_operations).mark_point().encode(
    x=alt.X('HourBin:O', title='Hour Bins'),
    y=alt.Y('count():Q', title='Number of Operations'),
    size=alt.Size('mean(Hours):Q', scale=alt.Scale(range=[100, 400]), title='Average Hours'),
    tooltip=[alt.Tooltip('HourBin:N', title='Hour Bin'), alt.Tooltip('count():Q', title='Ops Count'), alt.Tooltip('mean(Hours):Q', title='Avg Hours')]
).properties(
    title='Operation Count and Average Hours by Hour Bin'
)

chart.display()