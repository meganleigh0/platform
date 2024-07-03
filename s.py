limport streamlit as st
import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    "Hours": [1, 2, 0, 1.5, 0, 3],
    "Operation Description": ["Op1", "Op2", "", "Op3", "", "Op4"],
    "Department": ["Dept1", "Dept2", "", "Dept1", "", "Dept3"],
    "mbomID": [101, 102, 103, 101, 104, 105],
    "Assembly": ["Asm1", "Asm2", "Asm3", "Asm1", "Asm4", "Asm5"],
    "Variant": ["Var1", "Var2", "Var1", "Var2", "Var1", "Var3"],
    "Station": ["S1", "S2", "S1", "S2", "S3", "S1"]
}

df = pd.DataFrame(data)

# Streamlit App
st.title("Manufacturing Operations Dashboard")

variant = st.selectbox("Select Variant", df["Variant"].unique())
station = st.selectbox("Select Station", df["Station"].unique())

filtered_df = df[(df["Variant"] == variant) & (df["Station"] == station)]

st.subheader(f"Details for Variant: {variant} at Station: {station}")

operations_df = filtered_df[filtered_df["Operation Description"] != ""]
parts_df = filtered_df[filtered_df["Operation Description"] == ""]

st.write("### Operations")
st.write(operations_df[["Operation Description", "Hours", "Department", "Assembly"]])

st.write("### Parts")
st.write(parts_df[["mbomID", "Assembly"]])

st.write("### Assemblies")
assemblies_df = filtered_df[["Assembly", "mbomID"]].drop_duplicates()
st.write(assemblies_df)

# Visualizations
fig = px.bar(operations_df, x="Operation Description", y="Hours", color="Assembly", title="Operation Hours by Assembly")
st.plotly_chart(fig)

fig = px.pie(assemblies_df, names="Assembly", values="mbomID", title="Assemblies Distribution")
st.plotly_chart(fig)