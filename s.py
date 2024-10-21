import altair as alt
import pandas as pd

# Assuming your DataFrame 'df' is available
# Group the data by 'ActionCategory' and calculate total hours and count for each
df2 = df.groupby('ActionCategory').agg({'Hours': 'sum', 'ActionCategory': 'count'}).rename(columns={'ActionCategory': 'Count'}).reset_index()

# Sort the data by 'Hours' in descending order
df2 = df2.sort_values(by='Hours', ascending=False)

# Create a simple bar chart showing total Hours, sorted by Hours
chart = alt.Chart(df2).mark_bar(size=40).encode(
    x=alt.X('ActionCategory:N', title="Action Category", sort='-y', axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    y=alt.Y('Hours:Q', title="Total Hours", axis=alt.Axis(labelFontSize=14, titleFontSize=16)),
    color=alt.Color('ActionCategory:N', legend=None),  # Remove the legend for simplicity
    tooltip=['ActionCategory:N', 'Hours:Q', 'Count:Q']
).properties(
    title=alt.TitleParams(
        text="Total Hours and Count by Action Category",
        fontSize=18,
        anchor='start',
        offset=15
    ),
    width=600,
    height=400
)

# Add text labels for the Count on top of the bars
text = chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-5,  # Move text slightly above the bars
    fontSize=14,  # Increase font size for labels
    fontWeight='bold'  # Make the count labels bold
).encode(
    text='Count:Q'  # Show count as labels
)

# Display the final chart with the text layered on top
final_chart = (chart + text).configure_axis(
    grid=False  # Remove grid lines for a cleaner look
).configure_view(
    strokeWidth=0  # Remove the chart border
)

# Display the final chart
final_chart.display()


# Assuming `df2` is for the hours chart
# And `df3` is your word-processed operations dataframe

# Create the first chart (sorted by hours, like in the earlier step)
final_chart = (chart + text).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)

# Example bar chart for word-processed operations (df3)
operation_chart = alt.Chart(df3).mark_bar(size=40).encode(
    x=alt.X('CommonTerm:N', title="Common Operation Term"),
    y=alt.Y('Count:Q', title="Count"),
    color=alt.Color('CommonTerm:N', legend=None),
    tooltip=['CommonTerm:N', 'Count:Q']
).properties(
    title=alt.TitleParams(
        text="Common Operation Terms",
        fontSize=18,
        anchor='start',
        offset=15
    ),
    width=600,
    height=400
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
)

# Combine the two charts horizontally
combined_chart = alt.hconcat(final_chart, operation_chart)

# Display the combined chart
combined_chart.display()