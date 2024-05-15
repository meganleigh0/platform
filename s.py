import simpy

class Department:
    def __init__(self, env, name, num_employees):
        self.env = env
        self.name = name
        self.num_employees = num_employees
        self.worker_resource = simpy.Resource(env, capacity=num_employees)

env = simpy.Environment()
department1 = Department(env, 'Department 1', 10)
department2 = Department(env, 'Department 2', 10)
department3 = Department(env, 'Department 3', 10)
def employee_behavior(env, department, employee_id):
    with department.worker_resource.request() as request:
        yield request
        print(f'Employee {employee_id} in {department.name} starts working at {env.now}')
        yield env.timeout(10)  # Simulate work time
        print(f'Employee {employee_id} in {department.name} finishes work at {env.now}')
        
        def create_employees(env, department):
    for employee_id in range(department.num_employees):
        env.process(employee_behavior(env, department, employee_id))

env.process(create_employees(env, department1))
env.process(create_employees(env, department2))
env.process(create_employees(env, department3))

env.run(until=50)  # Run simulation for 50 time units