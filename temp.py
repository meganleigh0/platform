## Simulation Model Design for JSMC Manufacturing Process

### I. System Description:
  - **Simulation Scope:** From Hull & Turret Divorce to Final Delivery
  - **System Components:** Pre-Production, Plant 1 Operations, Plant 3 Assembly Line, Testing Phase, Final Delivery

### II. Entities:
  - **Units:**
    - Attributes: Type (Hull/Turret), Age, Status
  - **Parts:**
    - Attributes: Type, Quantity Available, Lead Time, Reorder Point
  - **Stations:**
    - Attributes: Type, Capacity, Assembly Requirement

### III. Processes:
  - **Pre-Production:**
    - Hull & Turret Divorce
  - **Plant 1 Operations:**
    - Hull Operations: Hull Tear Down, Hull Appurtenance, Hull Paint
    - Turret Operations: Removal of Turret Rails, Turret Machining, Turret Armor Attachment, Turret Appurtenances Attachment, Turret Painting
    - Fabrication: Cutting Operations, Welding Operations
  - **Plant 3 Assembly Line:**
    - Hull Assembly Line
    - Turret Assembly Line
    - Marriage & Final Assembly
  - **Testing Phase:**
    - QA & Inspection, Road Testing, Final Acceptance Testing
  - **Inventory Management:**
    - Ordering Process
    - Inventory Update
  - **Forecasting Process**

### IV. Resources:
  - **Inventory:** Tracked for each part
  - **Assembly Stations:** With specific capacities and assembly requirements

### V. Events:
  - **Part Order Placement**
  - **Part Order Arrival**

### VI. Data Inputs:
  - **Inventory Data:** Initial levels, reorder points, lead times
  - **Consumption Rates:** Rate of part consumption at each station

### VII. System States:
  - **Inventory Levels:** Dynamic tracking of each part's inventory

### VIII. Simulation Objectives:
  - **Planning & Tracking Tool:**
    - Effective scheduling and tracking of the entire manufacturing process
  - **Sensitivity/Risk Analysis:**
    - Analyze risks and sensitivities related to late part arrivals
  - **Inventory Optimization:**
    - Minimize holding costs, prevent shortages, optimize reorder points and quantities

### IX. Performance Metrics:
  - **Operational:**
    - Production Time
    - Throughput
    - Utilization of Stations
  - **Inventory:**
    - Holding Costs
    - Stockout Incidents (and use of Golden LRUs)
    - Order Placement Frequency


### X. Development Plan:
  - **Step 1:** Implement basic SimPy model
  - **Step 2:** Integrate Inventory Management
  - **Step 3:** Develop & integrate Forecasting Module
  - **Step 4:** Validate and Optimize the simulation model
  - **Step 5:** Implement GUI (using Flask or an alternative)
  - **Step 6:** Conduct comprehensive testing and validation

### XI. Implementation Approach:
  - Develop and validate in incremental steps
  - Ensure modularity for easy testing and validation of each component
  - Utilize historical data for validation and improvement of the simulation model
