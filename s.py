class Operation:
    def __init__(self, name):
        self.name = name
        self.is_completed = False

class Part:
    def __init__(self, name):
        self.name = name
        self.is_ready = False

class Assembly:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.operations = []

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

    def add_operation(self, operation):
        self.operations.append(operation)

    def check_readiness(self):
        if not all([op.is_completed for op in self.operations]):
            return False
        for child in self.children:
            if isinstance(child, Assembly) and not child.check_readiness():
                return False
            elif isinstance(child, Part) and not child.is_ready:
                return False
        return True

# Testing
part1 = Part("part1")
part2 = Part("part2")
part1.is_ready = True

assembly1 = Assembly("assembly1")
operation1 = Operation("operation1")
operation1.is_completed = True
assembly1.add_operation(operation1)
assembly1.add_child(part1)

assembly2 = Assembly("assembly2")
assembly2.add_child(assembly1)
assembly2.add_child(part2)

print(assembly2.check_readiness())  # This should print False since part2 is not ready

part2.is_ready = True
print(assembly2.check_readiness())  # Now, this should print True

