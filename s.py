import plotly.graph_objects as go

# Assuming plant_summary is your DataFrame
plant_fig = go.Figure(data=[
    go.Bar(
        name='Heads',
        x=plant_summary['Plant'],
        y=plant_summary['DirectHeads'],
        text=plant_summary['DirectHeads'],  # Add the text values for each bar
        textposition='outside'  # Position the text above the bars
    ),
    go.Bar(
        name='Heads Required',
        x=plant_summary['Plant'],
        y=plant_summary['Heads Required'],
        text=plant_summary['Heads Required'],  # Add the text values for each bar
        textposition='outside'  # Position the text above the bars
    )
])

# Update layout for grouped bar mode and title
plant_fig.update_layout(
    barmode='group',
    title="Heads vs Heads Required by Plant"
)

# Display plot (streamlit)
st.markdown("### Heads Required by Plant")
st.plotly_chart(plant_fig)
