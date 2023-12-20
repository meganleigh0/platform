def generate_calendar_style_schedule_table(schedule, highlight_month):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reindex(columns=month_order).reset_index()
    
    return pivot_df
Streamlit App with Month Selection and Highlighting
python
Copy code
# Streamlit layout
st.title("Production Schedule Simulator")

# Sidebar for user inputs
with st.sidebar:
    st.header("Simulation Settings")
    selected_month = st.selectbox("Select Month", options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    # ... Other inputs like duration and rate

# Main area
st.header("Production Schedule")
schedule_data = generate_calendar_style_schedule_table(simulation.schedule, selected_month)

# Apply the highlighting style for the selected month
def highlight_month(df, month):
    return [
        'background-color: #ff7f0e' if col == month else '' 
        for col in df.columns
    ]

st.dataframe(schedule_data.style.apply(highlight_month, month=selected_month))
