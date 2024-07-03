import streamlit as st
import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    "Hours": [1, 2, 0, 1.5, 0, 3, 0.5, 2, 0, 3, 1, 0],
    "Description": ["Assembly part", "Operation for assembly", "Part only", "Operation for assembly", "Part only", "Operation for assembly", "Operation for assembly", "Operation for assembly", "Part only", "Operation for assembly", "Operation for assembly", "Part only"],
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
    st.title('Manufacturing Dashboard')

    variant = st.sidebar.selectbox('Select Variant', options=df['Variant'].unique())
    station = st.sidebar.selectbox('Select Station', options=df['Station'].unique())

    filtered_data = df[(df['Variant'] == variant) & (df['Station'] == station)]

    if not filtered_data.empty:
        operations = filtered_data[filtered_data['Hours'] > 0]
        parts = filtered_data[filtered_data['Hours'] == 0]
        assemblies = filtered_data['Assembly'].unique()

        # Operations
        st.subheader(f'Operations at Station {station}')
        if not operations.empty:
            st.dataframe(operations[['Operation Description', 'Department', 'mbomID', 'Assembly']])
        else:
            st.write('No operations found for this selection.')

        # Parts
        st.subheader(f'Parts at Station {station}')
        if not parts.empty:
            st.dataframe(parts[['Description', 'mbomID', 'Assembly']])
        else:
            st.write('No parts found for this selection.')

        # Assemblies
        st.subheader(f'Assemblies at Station {station}')
        if assemblies.size > 0:
            st.write(assemblies)
        else:
            st.write('No assemblies found for this selection.')
    else:
        st.write("No data found for the selected variant and station.")

if __name__ == "__main__":
    main()