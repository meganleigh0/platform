# Function to sort months
def sort_months(months):
    month_order = ["January 2024", "February 2024", "March 2024", "April 2024", "May 2024", 
                   "June 2024", "July 2024", "August 2024", "September 2024", "October 2024", 
                   "November 2024", "December 2024"]
    sorted_months = [month for month in month_order if month in months]
    return sorted_months

# Function to calculate hours
def calculate_hours(requirements_df, schedule_df, selected_month=None, selected_program=None):
    filtered_schedule = schedule_df.copy()

    if selected_month:
        filtered_schedule = filtered_schedule[['Program', selected_month]]
    else:
        filtered_schedule = filtered_schedule[['Program'] + sort_months(list(schedule_df.columns[2:]))]

    if selected_program and selected_program != 'All Programs':
        filtered_schedule = filtered_schedule[filtered_schedule['Program'] == selected_program]

    merged_df = pd.merge(filtered_schedule, requirements_df, on='Program')
    total_hours_program = 0
    total_hours_vehicle = 0

    if selected_month:
        merged_df['Total Hours'] = merged_df[selected_month] * merged_df['Hours']
        total_hours_program = merged_df['Total Hours'].sum()
        if not merged_df[selected_month].empty:
            total_hours_vehicle = merged_df[selected_month].mean() * merged_df['Hours'].mean()
    else:
        for month in sort_months(list(schedule_df.columns[2:])):
            merged_df[month] = merged_df[month] * merged_df['Hours']
            total_hours_program += merged_df[month].sum()

    return merged_df, total_hours_vehicle, total_hours_program

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Production Schedule Analysis", anchor=None)

# Selection options
months = ['All Months'] + sort_months(list(schedule.columns[2:]))
programs = ['All Programs'] + list(schedule['Program'].unique())
selected_month = st.selectbox("Select a Month", months, index=0)
selected_program = st.selectbox("Select a Program", programs, index=0)

# Calculate hours for station and department
station_hours, station_vehicle_hours, station_program_hours = calculate_hours(station_requirements, schedule, selected_month if selected_month != 'All Months' else None, selected_program)
department_hours, department_vehicle_hours, department_program_hours = calculate_hours(department_requirements, schedule, selected_month if selected_month != 'All Months' else None, selected_program)

# Display the schedule for context
st.header("Production Schedule", anchor=None)
st.dataframe(schedule)

# Display results
st.header("Station and Department Hours", anchor=None)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Station Hours")
    if selected_month != 'All Months':
        st.bar_chart(station_hours.groupby('Station')['Total Hours'].sum())
    else:
        st.line_chart(station_hours.groupby('Station')[sort_months(schedule.columns[2:])].sum())

with col2:
    st.subheader("Department Hours")
    if selected_month != 'All Months':
        st.bar_chart(department_hours.groupby('DepartmentID')['Total Hours'].sum())
    else:
        st.line_chart(department_hours.groupby('DepartmentID')[sort_months(schedule.columns[2:])].sum())

# Display total hours for a vehicle and the program
if selected_month != 'All Months' and selected_program != 'All Programs':
    st.write(f"Total Hours for One Vehicle in {selected_program}: {station_vehicle_hours} (Station), {department_vehicle_hours} (Department)")
    st.write(f"Total Hours for Program {selected_program} in {selected_month}: {station_program_hours} (Station), {department_program_hours} (Department)")
