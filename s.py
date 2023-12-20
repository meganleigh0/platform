def generate_calendar_style_schedule_table(schedule, selected_month):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = schedule.months
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reindex(columns=month_order).reset_index()

    # Create a dictionary to apply custom styling to column headers
    header_style = {selected_month: 'background-color: #0074e4; color: white; font-weight: bold;'}

    # Apply the styling to the column headers
    styled_df = pivot_df.style.set_table_styles([{'selector': 'th', 'props': header_style}])
    return styled_df
