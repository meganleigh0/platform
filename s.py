# Streamlit layout
st.title("Production Schedule Simulator")

simulation = Simulation()  # Create a simulation instance

# Sidebar for user inputs
with st.sidebar:
    st.header("Simulation Settings")
    selected_month = st.selectbox("Select Month", options=simulation.schedule.months)
    duration = st.radio("Select Duration", options=['Day', 'Week', 'Month'], index=0)
    rate = st.number_input("Enter Rate", min_value=1, value=5)
    
    if st.button("Run Simulation"):
        # Run simulation logic with progress bar
        with st.spinner('Running Simulation...'):
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.1)  # Replace with actual simulation steps
                progress_bar.progress(percent_complete + 1)
            simulation.run_simulation(rate, {'Day': 1, 'Week': 7, 'Month': 30}[duration], selected_month)
            gantt_chart = go.Figure()  # Replace with actual function to generate Gantt chart
            st.session_state['gantt_chart'] = gantt_chart

    if st.button("Clear Simulation"):
        simulation.clear_simulation()
        st.session_state['gantt_chart'] = go.Figure()

# Main area
st.header("Production Schedule")
schedule_data = generate_calendar_style_schedule_table(simulation.schedule, selected_month)
st.dataframe(schedule_data)

# Display Gantt Chart
st.header("Gantt Chart Visualization")
if 'gantt_chart' in st.session_state:
    st.plotly_chart(st.session_state['gantt_chart'])
