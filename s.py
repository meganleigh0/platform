# 1. Identify unique sets by PlanNo and check for multiple Department occurrences
unique_plan_sets = df.groupby('PlanNo').filter(lambda x: len(x['Department'].unique()) > 1)

# 2. For PlanNos with multiple Departments, keep only the later sections
# This involves identifying the last occurrence of each PlanNo group with multiple Departments
last_occurrences = unique_plan_sets.drop_duplicates(subset=['PlanNo', 'Facility ID'], keep='last')
plan_no_to_keep = last_occurrences['PlanNo'].unique()

# 3. Keep rows that are either unique by PlanNo or are part of the later sections identified
filtered_df = pd.concat([
    df[df['PlanNo'].isin(plan_no_to_keep) == False],  # Unique PlanNos
    df[df['PlanNo'].isin(last_occurrences['PlanNo'])]  # Later sections of PlanNos with multiple Departments
]).drop_duplicates().sort_values(by=['PlanNo', 'Facility ID', 'Department'])

filtered_df
Result
