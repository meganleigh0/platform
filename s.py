import pandas as pd

def evaluate_production_feasibility(df, production_plan):
    # Calculate total required hours per department across all variants
    total_hours = df.groupby(['DepID', 'Name', 'DirectHeads', 'Plant']).apply(
        lambda x: sum(x['Hours'] * production_plan.get(x['Variant'], 0))
    ).reset_index(name='TotalRequiredHours')

    # Calculate potential hours (assuming 160 hours per month per head)
    total_hours['HoursPotential'] = total_hours['DirectHeads'] * 160

    # Calculate feasibility
    total_hours['Feasibility'] = total_hours['HoursPotential'] / total_hours['TotalRequiredHours']

    # Identify departments with feasibility issues
    underperforming_departments = total_hours[total_hours['Feasibility'] < 1]

    # Sort departments by feasibility to find the lowest outputting departments
    lowest_outputting_departments = underperforming_departments.sort_values('Feasibility')

    # Group by plant to see potential for reallocating heads
    plant_grouping = lowest_outputting_departments.groupby('Plant').apply(
        lambda x: x.sort_values(by='Feasibility')
    ).reset_index(drop=True)

    # Print lowest outputting departments
    print("Lowest outputting departments:")
    print(lowest_outputting_departments)

    # Print group by plant for insight on head reallocation
    print("\nInsights for head reallocation within plants:")
    print(plant_grouping)

    # Provide recommendations
    print("\nRecommendations:")
    if not underperforming_departments.empty:
        print("Consider reallocating resources or increasing headcounts in the following departments:")
        for index, row in lowest_outputting_departments.iterrows():
            print(f"- {row['Name']} in Plant {row['Plant']} (Feasibility: {row['Feasibility']:.2f})")
    else:
        print("All departments are meeting their production targets.")

# Sample DataFrame creation (replace this with your actual DataFrame)
data = {
    'Hours': [1, 2, 3, 4, 1, 2],
    'Operation Description': ['Assemble', 'Test', 'Pack', 'Assemble', 'Test', 'Pack'],
    'DepID': [101, 101, 102, 103, 103, 104],
    'Name': ['Assembly', 'Assembly', 'Packing', 'Assembly', 'Assembly', 'Packing'],
    'DirectHeads': [10, 10, 15, 20, 20, 15],
    'Plant': ['A', 'A', 'A', 'B', 'B', 'B'],
    'Variant': ['A', 'A', 'A', 'B', 'B', 'B']
}
df = pd.DataFrame(data)

# Example production plan
production_plan = {'A': 2, 'B': 1}

# Run the function
evaluate_production_feasibility(df, production_plan)