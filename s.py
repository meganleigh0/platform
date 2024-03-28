import pandas as pd

def analyze_plant_production(mbom_dfs):
    # Define plant codes and their product types
    plant_info = {
        'T': {'types': ['wiring harnesses', 'electronics'], 'codes': []},
        'A': {'types': ['reclaimed parts', 'Product S'], 'codes': ['AD', 'AG']},
        'J': {'types': ['welding/final assembly', 'Product A'], 'codes': []},
        'S': {'types': ['LRUS'], 'codes': []}
    }

    # Initialize a dictionary to hold the analysis results
    plant_analysis = {plant: {'products': [], 'count': 0} for plant in plant_info.keys()}

    # Process each product variant's dataframe
    for variant, df in mbom_dfs.items():
        # Check each part in the dataframe
        for index, row in df.iterrows():
            # Determine the plant based on 'Src Org' or 'Usr Org'
            for plant, info in plant_info.items():
                if any(code in row['Src Org'] or code in row['Usr Org'] for code in info['codes']):
                    plant_analysis[plant]['products'].append(row['PartNumber'])
                    plant_analysis[plant]['count'] += 1
                    break

    # Remove duplicates in product lists and count them
    for plant in plant_analysis.keys():
        plant_analysis[plant]['products'] = list(set(plant_analysis[plant]['products']))
        plant_analysis[plant]['count'] = len(plant_analysis[plant]['products'])

    return plant_analysis

# Usage example
# mbom_dfs = {
#     'variant1': pd.DataFrame({
#         'PartNumber': ['123', '456'],
#         'Description': ['Part A', 'Part B'],
#         'mbomID': ['001', '002'],
#         'ParentID': ['0', '001'],
#         'make/buy': ['make', 'buy'],
#         'Number of Children': [0, 1],
#         'Src Org': ['AD', 'J01'],
#         'Usr Org': ['A01', 'J01']
#     }),
#     'variant2': pd.DataFrame(...),
#     ...
# }
# 
# analysis_result = analyze_plant_production(mbom_dfs)
# print(analysis_result)