# Create a selection that will be shared by all charts
single_select = alt.selection_single(fields=['Program'], bind='legend', init={'Program': operators_by_program['Program'].iloc[0]})
