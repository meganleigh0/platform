def generate_calendar_style_schedule_table(schedule, highlight_month):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reset_index()
    pivot_df = pivot_df[['Program'] + month_order]  # Ensure months are in correct order

    # Apply styling
    def highlight_column(s):
        return ['background-color: lightgreen' if s.name == highlight_month else '' for _ in s]
    
    return pivot_df.style.apply(highlight_column, axis=0)
# Main area
st.header("Production Schedule")
schedule_data = generate_calendar_style_schedule_table(simulation.schedule, selected_month)
st.dataframe(schedule_data)
