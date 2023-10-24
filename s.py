example_mbom_data = {
    'Levels': [0,1,2,3,4,5,6,2,3,4,5,6,7,4],
    'PartNumber': [101,111,121,131,114,151,611,121,311,411,115,612,137,124],
    'Description': ['vehicle', 'final hull', 'hull 1', 'hull 0', 'hull paint', 'hull armor', 'divorce', 'turret 1', 'turret 0', 'turret paint', 'turret armor', 'turret mach', 'divorce', 'plate'],
    'Qty': [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    'Make/Buy': ['MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE','MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE', 'MAKE'],
    'mbomID': [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014],
    'ParentID': [0, 10001, 10002, 10003, 10004, 10005, 10006, 10002, 10008, 10009, 10010, 10011, 10012, 10008],
    'Number of Children': [1,2,1,1,1,1,0,2,1,1,1,1,0,0],
    'Station': ['vehilce', 'hull station 2', 'hull station 1', 'hull station 0', 'p1 hull', 'p1 hull', 'Divorce', 'turret station 1', 'turret station 0', 'p1 turret', 'p1 turret', 'p1 turret', 'Divorce', 'p1'],
    'Operations': [
        [[5, 'op1', 'depa'], [2, 'op2', 'depb']],
        [[1, 'op3', 'depc']],
        [[5, 'op4', 'depb']],
        [[5, 'op5', 'depa'], [2, 'op6', 'depb'], [1, 'op7', 'depa']],
        [[5, 'op8', 'depa'], [2, 'op9', 'depc'], [1, 'op10', 'depa']],
        [[5, 'op11', 'depa'], [2, 'op12', 'depb']],
        [[1, 'op13', 'depc']],
        [[5, 'op14', 'depb']],
        [[5, 'op15', 'depa'], [2, 'op16', 'depb'], [1, 'op17', 'depa']],
        [[5, 'op20', 'depa'], [2, 'op19', 'depc'], [1, 'op18', 'depa']],
        [[5, 'op21', 'depa'], [2, 'op22', 'depb']],
        [[1, 'op23', 'depc']],
        [[5, 'op24', 'depb']],
        [[5, 'op25', 'depa'], [2, 'op26', 'depb'], [1, 'op27', 'depa']],
    ]
}
mbom = pd.DataFrame(example_mbom_data)
mbom.to_csv('mbom.csv')
class Logger:
    def __init__(self):
        self.log = []

    def log_interaction(self, timestamp, interaction):
        self.log.append({'Timestamp': timestamp, 'Interaction': interaction})

    def visualize(self):
        times = [entry['Timestamp'] for entry in self.log]
        interactions = [entry['Interaction'] for entry in self.log]
        plt.plot(times, interactions, '-o')
        plt.xlabel("Time")
        plt.ylabel("Interactions")
        plt.title("Interaction Visualization")
        plt.grid(True)
        plt.show()

    def to_dataframe(self):
        return pd.DataFrame(self.log)

    def print_table(self):
        df = self.to_dataframe()
        print(df)

    def log_assy(self, timestamp, interaction, process, part_id):
        self.log.append({'Timestamp': timestamp, 'Interaction': interaction, 'Process': process, 'AssemblyID': part_id})

    def viz_assy(self):
        df = self.to_dataframe()
        fig = px.scatter(df, x="Timestamp", y="Interaction", color="Process")
        fig.show()


logger = Logger()
a_logger = Logger()

class Part:
    def __init__(self, env, part_id, part_num, name, qty, make_buy, station):
        self.env = env
        self.part_id = part_id
        self.part_num = part_num
        self.name = name 
        self.qty = qty
        self.make_buy = make_buy
        self.station = station
        self.children = []
        self.is_available = False

    def add_child(self, part):
        self.children.append(part)

    def check_availability(self):
        return all(child.processed for child in self.children)
    
    def set_as_unavailable(self):
        self.is_available = False

    def set_as_available(self):
        self.is_available = True            

class Assembly(Part):
    def __init__(self, env, part_id, part_num, name, qty, make_buy, station, operations, department_dict):
        super().__init__(env, part_id, part_num, name, qty, make_buy, station)
        self.children = []
        self.operations = []
        for operation in range(len(operations)):
            standard = operations[operation][0]
            name = operations[operation][1]
            department = operations[operation][2]
            self.operations.append(Operation(self.env, name, standard, department, department_dict))
        self.is_ready = self.check_all_children()
        self.completed = False

    def add_child(self, part):
        return super().add_child(part)
    
    def check_all_children(self):
        # Check if all operations are completed and all child parts are ready
        for child in self.children:
            if isinstance(child,Part):
                if not child.check_availability():
                    return False
            elif isinstance(child, Assembly):
                if not child.completed:
                    return False
            return True

    def process(self):
        if not self.is_ready:
            for child in self.children:
                # pre process children requirements
                if isinstance(child, Assembly) and not child.completed:
                    yield self.env.process(child.process())
        a_logger.log_assy(self.env.now, f"Starting Assebmly {self.name}", f"{self.station}", str(self.part_id))
        for operation in self.operations:
            yield self.env.process(operation.process())
        a_logger.log_assy(self.env.now, f"Finsihed Assebmly {self.name}", f"{self.station}", str(self.part_id))


class Operation:
    def __init__(self, env, name, standard, department, department_dict):
        self.env = env
        self.name = name
        self.standard = standard
        self.department = department_dict[department]
    
    def process(self):
        logger.log_interaction(self.env.now, f"Starting Operation {self.name}")
        yield self.env.timeout(float(self.standard))
        logger.log_interaction(self.env.now, f"Completed Operation {self.name}")

class Product:
    def __init__(self, env, name, parts):
        self.env = env
        self.name = name
        self.parts = parts

        self.plant1_parts = {k: v for k, v in self.parts.items() if 'p1' in v.station.lower()}
        self.plant3_parts = {k: v for k, v in self.parts.items() if 'p3' in v.station.lower()}
        self.vehicle_parts = {k: v for k, v in self.parts.items() if 'vehicle' in v.station.lower()}
        self.stations = self.extract_stations()

    def extract_stations(self):
        return set(part.station for part in self.parts.values())
    
class Hull:
    def __init__(self, env, hull_id, product):
        self.env = env
        self.id = hull_id
        
        self.p1_parts = {k: v for k, v in product.parts.items() if v.station.lower() == 'p1 hull'}

        self.p1_processed = False
        self.p3_processed = False

    def plant1_process(self, product):
        for part_or_assembly in self.p1_parts.values():
            if isinstance(part_or_assembly, Assembly):
                yield self.env.process(part_or_assembly.process())
        self.p1_processed = True

class Turret:
    def __init__(self, env, hull_id, product):
        self.env = env
        self.id = hull_id
        self.p1_parts = {k: v for k, v in product.parts.items() if v.station.lower() == 'p1 turret'}

        self.p1_processed = False
        self.p3_processed = False

    def plant1_process(self, product):
        for part_or_assembly in self.p1_parts.values():
            if isinstance(part_or_assembly, Assembly):
                yield self.env.process(part_or_assembly.process())
        self.p1_processed = True


class Structure:
    def __init__(self, env):
        self.id = uuid.uuid4()
        self.env = env
        self.divorced = False

    def divorce(self, product):
        ht_divorce_assemblies = [assembly for assembly in product.parts.values() if assembly.station == 'Divorce']
        for assembly in ht_divorce_assemblies:
            yield self.env.process(assembly.process())
        self.divorced = True
        hull_id = f"hull.{self.id}"
        turret_id = f"turret.{self.id}"
        self.hull = Hull(self.env, hull_id, product)
        self.turret = Turret(self.env, turret_id, product)

class Plant1:
    def __init__(self, env):
        self.env = env
        self.structures = []
        self.hulls = []
        self.turrets = []
        self.completed_hulls = []
        self.completed_turrets = []

    def add_structure(self):
        structure = Structure(self.env)
        self.structures.append(structure)
        print(f"Added structure {structure.id}")
        return structure
    
    def process_structure(self, structure, product):
        yield self.env.process(structure.divorce(product))
        hull = structure.hull
        turret = structure.turret
        yield self.env.process(hull.plant1_process(product)) | self.env.process(turret.plant1_process(product))

class Department:
    def __init__(self, env, id, name, head_count, plant, eff):
        self.env = env
        self.id = id
        self.name = name
        self.heads = simpy.Resource(env, capacity=head_count)
        self.plant = plant
        self.efficiency = eff
        self.completed_turrets = []

env = simpy.Environment()

example_dep_data = {
    'DepID': ['depa', 'depb', 'depc'],
    'Name': ['department blaha', 'department blahb', 'department blahc'],
    'HeadCount': [3,4,1],
    'Plant': [1, 1, 1],
    'Efficiency': [.78, .92, .85]
}
dep_data = pd.DataFrame(example_dep_data)

def load_departments(env):
    department_dict = {}
    df = dep_data 
    for _, row in df.iterrows():
        department = Department(env, row['DepID'], row['Name'], row['HeadCount'], row['Plant'], row['Efficiency'])
        department_dict[row['DepID']] = department
    return department_dict

department_dict = load_departments(env)

mbom = pd.read_csv('mbom.csv')

def parse_string(val):
    try:
        return ast.literal_eval(val)
    except (SyntaxError, ValueError):
        return val
    
mbom['Operations'] = mbom['Operations'].apply(parse_string)

sample_parts = {}
def load_porduct(mbom):
    for _, row in mbom.iterrows():
        if row['Operations']:
            sample_parts[row['mbomID']] = Assembly(env, row['mbomID'], row['PartNumber'], row['Description'], row['Qty'], row['Make/Buy'], row['Station'], row['Operations'], department_dict)
        else:
            sample_parts[row['mbomID']] = Part(env, row['mbomID'], row['PartNumber'], row['Description'], row['Qty'], row['Make/Buy'], row['Station'])


    for _, row in mbom.iterrows():
        mbom_id = row['mbomID']
        df_children = mbom[mbom['ParentID'] == mbom_id]
        children = df_children['mbomID'].values
        for child in children:
            child_part = sample_parts[child]
            sample_parts[mbom_id].add_child(child_part)
    
    product = Product(env, 'sample', sample_parts)
    return product

product_1 = load_porduct(mbom)


plant1_simulation = Plant1(env)

structure_1 = plant1_simulation.add_structure()

env.process(plant1_simulation.process_structure(structure_1, product_1))

env.run(until=25)
logger.print_table()
a_logger.viz_assy()
