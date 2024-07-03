# Load the data into a DataFrame
df = pd.DataFrame(data)

# Streamlit application
def main():
    st.title('Manufacturing Operations Dashboard')
    
    # Sidebar selections
    variant = st.sidebar.selectbox('Select Variant', options=df['Variant'].unique())
    station = st.sidebar.selectbox('Select Station', options=df['Station'].unique())

    # Filter data based on selections
    filtered_data = df[(df['Variant'] == variant) & (df['Station'] == station)]
    
    # Separate operations and parts
    operations = filtered_data[filtered_data['Hours'] > 0]
    parts = filtered_data[filtered_data['Hours'] == 0]

    # Display Operations
    if not operations.empty:
        st.subheader('Operations at Station ' + station)
        st.write(operations[['Operation Description', 'Department', 'mbomID', 'Assembly']])
        # Plotting with Plotly for visual insight
        fig = px.bar(operations, x='Operation Description', y='Hours', color='Department', title='Operation Hours by Department')
        st.plotly_chart(fig)
    else:
        st.subheader('No operations found for this selection.')

    # Display Parts
    if not parts.empty:
        st.subheader('Parts at Station ' + station)
        st.write(parts[['mbomID', 'Assembly']])
    else:
        st.subheader('No parts found for this selection.')

    # Display Assemblies involved in selected Station
    assemblies = filtered_data['Assembly'].unique()
    if assemblies.size > 0:
        st.subheader('Assemblies at Station ' + station)
        st.write(assemblies)
    else:
        st.subheader('No assemblies found for this selection.')

# Run the Streamlit application
if __name__ == "__main__":
    main()