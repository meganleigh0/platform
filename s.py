    # Total heads and heads required
    total_heads = df_department_data['Heads'].sum()
    total_heads_required = plant_needs['Heads Required'].sum()

    # Donut chart for total heads vs heads required
    fig_donut = px.pie(names=["Total Heads", "Total Heads Required"], 
                       values=[total_heads, total_heads_required], 
                       hole=0.4, 
                       title="Overall Heads vs Heads Required")
    st.plotly_chart(fig_donut)
