import simpy

# Define a function to simulate the operations at a station
def operation(env, operation, station, part):
    yield env.timeout(operation['Hours'])
    print(f"Completed {operation['Description']} for {part['Description']} at {station['Description']} at time {env.now}")

# Initialize the simulation environment
env = simpy.Environment()

# Create resources for each station
stations = {}
for index, row in stations_df.iterrows():
    parallel = row['ParallelProcessing']
    capacity = float('inf') if parallel else 1
    stations[row['StationID']] = simpy.Resource(env, capacity=capacity)

# Define a function to process a part and its children
def process_part(env, part_number):
    part = parts_df[parts_df['PartNumber'] == part_number].iloc[0]
    child_parts = parts_df[parts_df['ParentPart'] == part_number]
    
    # Process child parts first
    for index, child in child_parts.iterrows():
        yield env.process(process_part(env, child['PartNumber']))
    
    # Process the part itself
    part_operations = part_operations_df[part_operations_df['PartNumber'] == part_number]
    for index, row in part_operations.iterrows():
        operation = operations_df[operations_df['OperationID'] == row['OperationID']].iloc[0]
        station = stations_df[stations_df['StationID'] == operation['StationID']].iloc[0]
        station_resource = stations[operation['StationID']]
        
        with station_resource.request() as request:
            yield request
            yield env.process(operation(env, operation, station, part))

# Schedule the initial parts
initial_parts = parts_df[parts_df['ParentPart'].isna()]
for index, part in initial_parts.iterrows():
    env.process(process_part(env, part['PartNumber']))

# Run the simulation
env.run()