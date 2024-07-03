import streamlit as st
import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    "Hours": [1, 2, 0, 1.5, 0, 3, 0.5, 2, 0, 3, 1, 0],
    "Operation Description": ["Op1", "Op2", "", "Op3", "", "Op4", "Op5", "Op6", "", "Op7", "Op1", ""],
    "Department": ["Dept1", "Dept2", "", "Dept1", "", "Dept3", "Dept1", "Dept2", "", "Dept3", "Dept1", ""],
    "mbomID": [101, 102, 103, 101, 104, 105, 106, 107, 108, 109, 110, 111],
    "Assembly": ["Asm1", "Asm2", "Asm3", "Asm1", "Asm4", "Asm5", "Asm1", "Asm2", "Asm3", "Asm5", "Asm1", "Asm4"],
    "Variant": ["Var1", "Var2", "Var1", "Var2", "Var1", "Var3", "Var1", "Var2", "Var3", "Var2", "Var1", "Var2"],
    "Station": ["S1", "S2", "S1", "S2", "S3", "S1", "S1", "S2", "S1", "S2", "S3", "S1"]
}

df = pd.DataFrame(data)

def main():
    st.set_page_config(layout="wide")
    st.title('Manufacturing Operations Dashboard')

    # Landing page showing total labor by variant
    st.markdown("## Total Labor by Variant")
    labor_by_variant = df.groupby('Variant')['Hours'].sum().reset_index()
    fig_total_labor = px.bar(labor_by_variant, x='Variant', y='Hours', title='Total Labor Hours by Variant')
    st.plotly_chart(fig_total_labor, use_container_width=True)

    # Sidebar selections
    variant = st.sidebar.selectbox('Select Variant', options=df['Variant'].unique())
    station = st.sidebar.selectbox('Select Station', options=df['Station'].unique())

    # Filter data based on selections
    filtered_data = df[(df['Variant'] == variant) & (df['Station'] == station)]

    st.markdown("### Operations at Station " + station)
    operations = filtered_data[filtered_data['Hours'] > 0]
    if not operations.empty:
        st.write(operations[['Operation Description', 'Department', 'mbomID', 'Assembly']])
    else:
        st.write("No operations found for this selection.")

    st.markdown("### Parts at Station " + station)
    parts = filtered_data[filtered_data['Hours'] == 0]
    if not parts.empty:
        st.write(parts[['mbomID', 'Assembly']])
    else:
        st.write("No parts found for this selection.")

    st.markdown("### Assemblies at Station " + station)
    assemblies = filtered_data['Assembly'].unique()
    if assemblies.size > 0:
        st.write(assemblies)
    else:
        st.write("No assemblies found for this selection.")

if __name__ == "__main__":
    main()