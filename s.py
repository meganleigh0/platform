import altair as alt

# Assuming all_operations is already loaded as a DataFrame

# 1. Adjusted Chart for Top 5 Longest Operations by Variant
# First, calculate a rank for each operation within each variant based on Hours
ranked_operations = alt.Chart(all_operations).transform_window(
    rank='rank(Hours)',
    sort=[alt.SortField('Hours', order='descending')],
    groupby=['Variant']
).transform_filter(
    (alt.datum.rank <= 5)  # Filter to top 5
)

# Then, create the bar chart
chart1_adjusted = ranked_operations.mark_bar().encode(
    x=alt.X('Variant:N', sort='-y'),
    y=alt.Y('Hours:Q', title='Hours per Operation'),
    color='Variant:N',
    tooltip=['Operation Description', 'Hours']
).properties(title="Top 5 Longest Operations by Variant")

# 2. Adjusted Station Workload Chart, sorted by Station
chart3_adjusted = alt.Chart(all_operations).mark_bar().encode(
    x=alt.X('Station:N', sort='ascending'),  # Adjust sort here if station names are sortable
    y='sum(Hours):Q',
    color='Variant:N',
    tooltip=['Station', 'sum(Hours)']
).properties(title="Workload Distribution by Station")

# 3. Adjusted Chart for Part Number Repetitions, with Title and Descending Order
chart5_adjusted = alt.Chart(all_operations).mark_bar().encode(
    x=alt.X('PartNumber:N', sort='-y'),  # Sorting by count, descending
    y=alt.Y('count(PartNumber):Q', title='Frequency'),
    color='Variant:N',
    tooltip=['PartNumber', 'count(PartNumber)']
).properties(title="Part Number Frequency in Operations")

# Example of how to view one of the adjusted charts
chart1_adjusted.display()