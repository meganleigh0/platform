import altair as alt

# Assuming all_operations is already loaded into a DataFrame

# Step 1: Add a calculated field for custom bubble sizes
chart2 = alt.Chart(all_operations).transform_calculate(
    bubbleSize="if(datum.Hours <= 2, 50, if(datum.Hours <= 5, 100, if(datum.Hours <= 10, 200, 300)))"
).mark_point().encode(
    x='Hours:Q',
    y='Variant:N',
    color='Variant:N',
    size=alt.Size('bubbleSize:Q', scale=alt.Scale(range=[50, 300]), legend=alt.Legend(title="Custom Hour Bins")),
    tooltip=['Operation Description', 'Hours']
).properties(title="Operation Similarities Across Variants")

chart2.display()