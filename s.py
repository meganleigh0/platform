import csv

# Read MBOM data from mbom.csv
mbom_data = {}
with open('mbom.csv', newline='') as mbom_file:
    reader = csv.DictReader(mbom_file)
    for row in reader:
        mbom_data[row['PartNumber']] = row

# Read Operation Sheet data from operation_sheet.csv
operation_data = {}
with open('operation_sheet.csv', newline='') as operation_file:
    reader = csv.DictReader(operation_file)
    for row in reader:
        operation_data[row['PlanNumber']] = row

# Create part_operation_links based on FacilityID
part_operation_links = {}
for part_number, part_data in mbom_data.items():
    facility_id = int(input(f"Enter FacilityID for PartNumber {part_number}: "))  # User input for FacilityID
    part_operation_links[part_number] = {
        'FacilityID': facility_id,
        'PlanNumbers': []  # Initialize empty list for PlanNumbers
    }

# Populate PlanNumbers based on FacilityID
for plan_number, operation_data in operation_data.items():
    facility_id = int(operation_data['FacilityID'])
    for part_number, part_link_data in part_operation_links.items():
        if part_link_data['FacilityID'] == facility_id:
            part_link_data['PlanNumbers'].append(plan_number)

# Print the created part_operation_links
print(part_operation_links)
