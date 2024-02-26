import simpy

def process(env, name, priority_resource, priority):
    with priority_resource.request(priority=priority) as req:
        yield req
        print(f"{name} obtained resource at {env.now}")
        yield env.timeout(1)
        print(f"{name} released resource at {env.now}")

env = simpy.Environment()
priority_resource = simpy.PriorityResource(env, capacity=1)

env.process(process(env, 'Process A', priority_resource, priority=0))
env.process(process(env, 'Process B', priority_resource, priority=2))
env.process(process(env, 'Process C', priority_resource, priority=1))

env.run(until=10)