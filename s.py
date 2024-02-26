    # Initialize an empty list to collect expanded rows
    expanded_rows = []

    # Manually expand the 'Operations' list into separate rows
    for index, row in self.df_lim.iterrows():
        if row['Operations']:
            for operation in row['Operations']:
                expanded_row = row.to_dict()
                expanded_row['Operation Hours'] = operation[0]
                expanded_row['Department'] = operation[2]
                expanded_rows.append(expanded_row)
        else:
            expanded_row = row.to_dict()
            expanded_row['Operation Hours'] = None
            expanded_row['Department'] = None
            expanded_rows.append(expanded_row)
