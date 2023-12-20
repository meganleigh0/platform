def generate_calendar_style_schedule_table(schedule, selected_month):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = schedule.months
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reindex(columns=month_order).reset_index()

    # Function to apply the highlighting style
    def highlight_selected_month(s):
        if s.name == selected_month:
            return ['background-color: #ff7f0e' for _ in s]
        else:
            return ['' for _ in s]

    # Apply the styling to the DataFrame
    styled_df = pivot_df.style.apply(highlight_selected_month)
    return styled_df
