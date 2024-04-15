assembly_line.py & SimComponents_assembly_line.py:
These files seem to define the simulation components and logic for an assembly line system. Key elements include managing different stages of the assembly process, handling events like starting and finishing tasks, and possibly inter-process communication.
block_assembly.py & SimComponents_for_block_assembly.py:
These are likely to focus on specific block assembly processes within a manufacturing setup. It might simulate the workflow within a particular section of the factory, tracking block processing times, order of operations, and the movement between different assembly stages. masterplan.py & SimComponents_for_masterplan.py:
This pair of files might represent a higher-level view of a production or project plan. This could include integration of various smaller processes into a larger framework, managing dependencies, and scheduling.
supply_chain.py & SimComponents_for_supply_chain.py:
Common Components
Most files rely on shared simulation components, which are defined across multiple SimComponents_*.py files. These components typically include classes for Part, Source, Sink, Process, and Monitor, with variations like DataframePart and DataframeSource which likely handle data-driven aspects of the simulation.
Source: This class probably generates new parts or jobs in the simulation.
Sink: Typically collects finished parts or jobs, handling their removal from the simulation. Process: Represents a step or operation in the manufacturing or supply chain, handling the logic for processing parts.
Monitor: Likely used for logging or tracking the state of various components in the simulation. Part/DataframePart: Represents the items being manufactured or processed.
File-Specific Details
assembly_line.py & SimComponents_assembly_line.py: These files appear to set up a basic assembly line simulation, importing core simulation components like Source, Sink, Process, and Monitor. The assembly_line.py might be directly executable and includes the main logic to run the simulation.
block_assembly.py & SimComponents_for_block_assembly.py: Focus on block assembly processes, including more specific tasks and handling, such as converting data from Excel files (indicated by csv_from_excel function). It uses customized simulation components for block assembly scenarios.
masterplan.py & SimComponents_for_masterplan.py: These files handle the overarching planning and scheduling aspects of the simulation. Functions like gen_schedule and gen_block_data suggest generation and management of data related to scheduling and block operations within a larger plan.

 supply_chain.py & SimComponents_for_supply_chain.py: These files handle the supply chain aspects of the simulation, including inventory and logistics management, possibly tracking the flow of materials from suppliers to the manufacturing processes.
Interaction and Flow
The main simulation files (*.py without SimComponents) utilize the components defined in their corresponding SimComponents_*.py files to build specific parts of the system, like an assembly line or a supply chain model.
They might each run independently for different simulations or be part of a larger system where data and results from one simulation feed into another—e.g., output from supply_chain.py could