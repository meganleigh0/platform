# Prepare DataFrame
for station in summary_data:
    summary_data[station]['Departments'] = ', '.join(sorted(str(dept) for dept in summary_data[station]['Departments']))
summary_df = pd.DataFrame.from_dict(summary_data, orient='index', columns=['Parts', 'Assemblies', 'Operations', 'Total Operation Hours', 'Departments'])
