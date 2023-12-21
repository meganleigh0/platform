# Load data
df = pd.read_csv('logs/assembly.csv')
df['Duration'] = round(df['Timestamp_end'] - df['Timestamp_start'], 2)

# Page title
st.title("Vehicle Assembly Data Visualization")

# Sidebar for vehicle selection
st.sidebar.header("Vehicle Selection")
vehicle = st.sidebar.selectbox("Choose a Vehicle", df['Vehicle'].unique())
filtered_df = df[df['Vehicle'] == vehicle]

# Station Utilization Bar Chart
st.subheader("Station Utilization Overview")
station_count = filtered_df['Station'].value_counts()
fig1 = px.bar(station_count, labels={'index': 'Station', 'value': 'Assembly Count'})
fig1.update_layout(title='Station Assembly Count', yaxis_title='Assembly Count', width=1000)
st.plotly_chart(fig1)

# Assembly Duration Scatter Plot
st.subheader("Assembly Duration Analysis")
fig2 = px.scatter(filtered_df, x='Station', y='Duration', color='Assembly')
fig2.update_layout(title='Assembly Duration per Station', width=1000)
st.plotly_chart(fig2)

# Workflow Time Series
st.subheader("Workflow Time Series")
fig3 = px.line(filtered_df, x='Timestamp_start', y='Assembly')
fig3.update_layout(title='Workflow Time Series', width=1000)
st.plotly_chart(fig3)

# Data Table
st.subheader("Detailed Data View")
st.write(filtered_df)
