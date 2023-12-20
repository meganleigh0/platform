python
Copy code
def generate_calendar_style_schedule_table(schedule, selected_year, highlight_month):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for date, quantity in program_obj.production_plan.items():
            year, month = date.split('-')  # Assuming the format is 'YYYY-MM'
            if year == selected_year:
                data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reindex(columns=month_order).reset_index()
    
    # Apply styling
    def highlight_column(s):
        return ['background-color: lightgreen' if s.name == highlight_month else '' for _ in s]
    
    return pivot_df.style.apply(highlight_column, axis=0)
In this updated function:

The function now takes an additional selected_year parameter.
The data is filtered to include only the entries for the selected year.
The months are ordered as per your list.
Now, let's update the Streamlit application to include year selection:

python
Copy code
# Streamlit layout
st.title("Production Schedule Simulator")

# Sidebar for user inputs
with st.sidebar:
    st.header("Simulation Settings")
    selected_year = st.selectbox("Select Year", options=['2024', '2025', '2026'])
    selected_month = st.selectbox("Select Month", options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    duration = st.radio("Select Duration", options=['Day', 'Week', 'Month'], index=0)
    rate = st.number_input("Enter Rate", min_value=1, value=5)
    
    if st.button("Run Simulation"):
        # Run simulation logic with progress bar
        # ...

    if st.button("Clear Simulation"):
        # Clear simulation logic
        # ...

# Main area
st.header("Production Schedule")
schedule_data = generate_calendar_style_schedule_table(simulation.schedule, selected_year, selected_month)
st.dataframe(schedule_data)

# Display Gantt Chart
