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










To track different operations for parts at different plants based on Usr Org and Src Org, you can extend the part_operation_links data structure to include organization-specific operation links. Here's an example of how you might modify the structure:

python
Copy code
# Define the MBOM data with organization-specific information
mbom_data = {
    "1234": {"Description": "Widget A", "MakeBuy": "Make", "UsrOrg": "Org1", "SrcOrg": "Org2"},
    "5678": {"Description": "Widget B", "MakeBuy": "Buy", "UsrOrg": "Org3", "SrcOrg": "Org4"},
    # Add more PartNumbers as needed
}

# Define the operation sheet data with facility and organization information
operation_data = {
    "OP001": {"Description": "Assembly", "Hours": 2, "FacilityID": 1, "UsrOrg": "Org1", "SrcOrg": "Org2"},
    "OP002": {"Description": "Testing", "Hours": 1, "FacilityID": 2, "UsrOrg": "Org3", "SrcOrg": "Org4"},
    # Add more PlanNumbers as needed
}

# Define the link between PartNumbers and PlanNumbers based on FacilityID, UsrOrg, and SrcOrg
part_operation_links = {
    "1234": {
        "FacilityID": 1,
        "OrganizationLinks": {
            "Org1_Org2": ["OP001", "OP002"],  # PartNumber 1234 operations for UsrOrg: Org1, SrcOrg: Org2
            # Add more organization-specific links as needed
        }
    },
    "5678": {
        "FacilityID": 2,
        "OrganizationLinks": {
            "Org3_Org4": ["OP001"],  # PartNumber 5678 operations for UsrOrg: Org3, SrcOrg: Org4
            # Add more organization-specific links as needed
        }
    },
    # Add more links as needed
}
In this modified structure:

operation_data now includes UsrOrg and SrcOrg information along with FacilityID for each operation.
part_operation_links includes organization-specific links (OrganizationLinks) for each part, where the key is a combination of UsrOrg and SrcOrg separated by an underscore.
With this structure in place, you can track different operations for parts at different plants based on Usr Org and Src Org. When a facility needs to determine the order of operations for a part based on its organization, it can access the relevant OrganizationLinks in part_operation_links.

Here's how you might access organization-specific operations for a part at a facility:

python
Copy code
# Assume facility_id, part_number, usr_org, and src_org are known
facility_id = 1  # Example FacilityID
part_number = '1234'  # Example PartNumber
usr_org = 'Org1'  # Example UsrOrg
src_org = 'Org2'  # Example SrcOrg

# Get the part_operation_links for the specified part
part_links = part_operation_links.get(part_number, {})
if part_links and part_links['FacilityID'] == facility_id:
    # Get the organization-specific links for the specified organization
    org_links = part_links['OrganizationLinks'].get(f"{usr_org}_{src_org}", [])
    
    # Print the organization-specific operations
    print(f"Organization-specific operations for PartNumber {part_number} at FacilityID {facility_id} with UsrOrg: {usr_org}, SrcOrg: {src_org}:")
    for plan_number in org_links:
        operation_data = operation_data.get(plan_number, {})
        if operation_data:
            print(f"PlanNumber: {plan_number}, Description: {operation_data['Description']}, Hours: {operation_data['Hours']}")
else:
    print(f"No operations found for PartNumber {part_number} at FacilityID {facility_id}.")
This code checks for organization-specific operations for a part at a facility based on UsrOrg and SrcOrg. It retrieves the relevant OrganizationLinks for the specified organization and prints the corresponding operations.
