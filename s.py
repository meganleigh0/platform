# Load your data
df = pd.read_csv('logs/assembly.csv')
df['Duration'] = round(df['Timestamp_end'] - df['Timestamp_start'], 2)

# Sidebar for vehicle selection
vehicle = st.sidebar.selectbox("Select Vehicle", df['Vehicle'].unique())
filtered_df = df[df['Vehicle'] == vehicle]

# Dashboard Title
st.title("Manufacturing Simulation Dashboard")

# Station Utilization Bar Chart
station_count = filtered_df['Station'].value_counts()
fig1 = px.bar(station_count)
st.plotly_chart(fig1)

# Assembly Duration Scatter Plot
fig2 = px.scatter(filtered_df, x='Station', y='Duration', color='Assembly')
st.plotly_chart(fig2)

# Workflow Time Series
fig3 = px.line(filtered_df, x='Timestamp_start', y='Assembly')
st.plotly_chart(fig3)

# Data Table
st.write(filtered_df)
