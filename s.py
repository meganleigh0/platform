from enum import Enum

class Status(Enum):
    NOT_STARTED = 1
    IN_PROCESS = 2
    COMPLETED = 3

class Assembly(Part):
    def __init__(self, ...):  # Existing initialization
        ...
        self.status = Status.NOT_STARTED

    def process(self):
        # If the assembly is completed or in process, return
        if self.status == Status.COMPLETED or self.status == Status.IN_PROCESS:
            return
        
        # Mark the assembly as in process
        self.status = Status.IN_PROCESS
        print(f"Attempting to Process Assembly: {self.name}")

        # Recursively process children assemblies first
        for child in self.children:
            if isinstance(child, Assembly) and child.status != Status.COMPLETED:
                child.process()
            elif isinstance(child, Part) and not child.is_ready:
                child.process()

        # Now, process the operations for this assembly
        if self.check_readiness():
            for operation in self.operations:
                operation.process()
            print(f"Processing operations for Assembly: {self.name}")
            
        # Mark the assembly as completed
        self.status = Status.COMPLETED
