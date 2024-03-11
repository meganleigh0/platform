import altair as alt

# Assuming all_operations is already loaded into a DataFrame

# Define the bubble sizes based on the bins
def bubble_size(hour):
    if hour <= 10:
        return 100
    elif hour <= 20:
        return 200
    elif hour <= 100:
        return 300
    else:
        return 400

# Apply the bubble sizes
chart2_updated = alt.Chart(all_operations).transform_bin(
    ['hourBin'], field='Hours', bin=alt.Bin(maxbins=4, extent=[0, 100])
).transform_aggregate(
    total_hours='sum(Hours)', groupby=['hourBin']
).transform_calculate(
    bubbleSize="if(datum.hourBin <= 10, 100, if(datum.hourBin <= 20, 200, if(datum.hourBin <= 100, 300, 400)))"
).mark_point().encode(
    x=alt.X('hourBin:N', title='Hour Bins'),
    y=alt.Y('total_hours:Q', aggregate='sum', title='Total Hours'),
    size=alt.Size('bubbleSize:Q', scale=alt.Scale(range=[100, 400]), legend=alt.Legend(title="Hours")),
    tooltip=['hourBin', 'total_hours']
).properties(title="Operation Similarities Across Variants by Hour Bins")

chart2_updated.display()