# Calculate the total heads required and total heads available
total_heads_required = plant_summary['Heads Required'].sum()
total_heads_available = plant_summary['Heads'].sum()

# Calculate the delta
delta = total_heads_available - total_heads_required

# Determine the color based on delta (shortfall or surplus)
if delta >= 0:
    color = 'green'  # Surplus, color it green
else:
    color = 'red'    # Shortfall, color it red

# Create the gauge chart
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=total_heads_available,
    delta={"reference": total_heads_required},
    gauge={
        "axis": {"range": [None, max(total_heads_required, total_heads_available)]},
        "threshold": {
            "line": {"color": color, "width": 4},
            "thickness": 0.75,
            "value": total_heads_required
        },
        "steps": [
            {"range": [0, total_heads_required], "color": "red"},
            {"range": [total_heads_required, total_heads_available], "color": "green"}
        ],
        "bar": {"color": color}
    },
))

fig.update_layout(title="Total Heads Required vs Total Heads Available",
                  showlegend=False)

st.plotly_chart(fig)
