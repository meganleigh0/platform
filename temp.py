from graphviz import Digraph

dot = Digraph(comment='The JSMC Production Process')

# Main Process Nodes
dot.node('A', 'Pre-Production')
dot.node('B', 'Initial Preparation')
dot.node('C', 'Fabrication')
dot.node('D', 'Assembly Line')
dot.node('E', 'Testing Phase')
dot.node('F', 'Final Delivery')

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF'])

# Sub-nodes for Initial Preparation
dot.node('BA', 'Shot Blasting')
dot.node('BB', 'Painting and De-Masking')
dot.edges(['BBA', 'ABB'])  # Connect sub-nodes to main node B

# Sub-nodes for Fabrication
dot.node('CA', 'Cutting Operations')
dot.node('CB', 'Welding Operations')
dot.edges(['CCA', 'BCC'])  # Connect sub-nodes to main node C

# Sub-nodes for Assembly Line
dot.node('DA', 'Hull Assembly')
dot.node('DB', 'Turret Assembly')
dot.node('DC', 'Final Assembly')
dot.edges(['DDA', 'CDD', 'DDB', 'DDC'])  # Connect sub-nodes to main node D

# Sub-nodes for Testing Phase
dot.node('EA', 'QA & Inspection')
dot.node('EB', 'Road Testing')
dot.node('EC', 'Final Acceptance Testing')
dot.edges(['EEA', 'DEE', 'EEB', 'EEC'])  # Connect sub-nodes to main node E

dot.render('jsmc_process.gv', view=True)  # Output: jsmc_process.gv.pdf
