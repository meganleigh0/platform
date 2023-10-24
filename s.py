class Assembly:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.operations = []

    def add_child(self, child):
        self.children.append(child)

    def add_operation(self, operation):
        self.operations.append(operation)

    def process(self):
        # Check and process only unprocessed children
        for child in self.children:
            if isinstance(child, Assembly):
                while not child.check_readiness():
                    print(f"Processing Assembly: {child.name}")
                    child.process()
                    print(f"Assembly {child.name} readiness after processing: {child.check_readiness()}")
            elif isinstance(child, Part) and not child.is_ready:
                child.process()

        # After processing required children, process the operations of this assembly
        for operation in self.operations:
            operation.is_completed = True

    def check_readiness(self):
        # Check if all operations of this assembly are completed
        if not all([op.is_completed for op in self.operations]):
            return False
        # Check the readiness of children
        for child in self.children:
            if isinstance(child, Assembly) and not child.check_readiness():
                print(f"Assembly {self.name} process child {child.name}")
                return False
            elif isinstance(child, Part) and not child.is_ready:
                return False
        return True
