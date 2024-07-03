import streamlit as st
import pandas as pd
import plotly.express as px

# Example DataFrame
data = {
    "Hours": [1, 2, 0, 1.5, 0, 3, 0, 2, 0, 3, 1, 0],
    "Operation Description": ["Op1", "Op2", "", "Op3", "", "Op4", "", "Op6", "", "Op7", "Op1", ""],
    "Department": ["Dept1", "Dept2", "", "Dept1", "", "Dept3", "", "Dept2", "", "Dept3", "Dept1", ""],
    "mbomID": [101, 102, 103, 101, 104, 105, 106, 107, 108, 109, 110, 111],
    "Description": ["Asm1 part", "Asm2 part", "Part A", "Asm2 part", "Part B", "Asm5 part", "Part C", "Asm2 part", "Part D", "Asm5 part", "Asm1 part", "Part E"],
    "Variant": ["Var1", "Var2", "Var1", "Var2", "Var1", "Var3", "Var1", "Var2", "Var3", "Var2", "Var1", "Var2"],
    "Station": ["S1", "S2", "S1", "S2", "S3", "S1", "S1", "S2", "S1", "S2", "S3", "S1"]
}

df = pd.DataFrame(data)

def main():
    st.set_page_config(layout="wide")
    st.title('Manufacturing Dashboard')

    # Displaying the sum of hours by department for each variant
    st.markdown("## Summary of Hours by Department and Variant")
    operation_data = df[df['Hours'] > 0]  # Filter out parts (0 hours)
    summary_df = operation_data.groupby(['Variant', 'Department'])['Hours'].sum().reset_index()
    fig = px.bar(summary_df, x='Variant', y='Hours', color='Department', title="Total Hours by Department for Each Variant", labels={"Hours": "Total Hours"})
    st.plotly_chart(fig, use_container_width=True)

    # Sidebar for selecting variant and station
    variant = st.sidebar.selectbox('Select Variant', options=df['Variant'].unique())
    station = st.sidebar.selectbox('Select Station', options=df['Station'].unique())

    # Filter data based on the selection
    filtered_data = df[(df['Variant'] == variant) & (df['Station'] == station)]

    # Display operations at the selected station
    st.markdown("### Operations at Station " + station)
    operations = filtered_data[(filtered_data['Hours'] > 0)]
    if not operations.empty:
        st.dataframe(operations[['Operation Description', 'Department', 'mbomID', 'Description']], width=700)
    else:
        st.write('No operations found for this selection.')

    # Display parts at the selected station
    st.markdown("### Parts at Station " + station)
    parts = filtered_data[(filtered_data['Hours'] == 0)]
    if not parts.empty:
        st.dataframe(parts[['mbomID', 'Description']], width=700)
    else:
        st.write('No parts found for this selection.')

    # Display assemblies at the selected station
    st.markdown("### Assemblies at Station " + station)
    assemblies = operations['Description'].unique()
    if assemblies.size > 0:
        st.write(", ".join(assemblies))
    else:
        st.write("No assemblies found for this selection.")

if __name__ == "__main__":
    main()