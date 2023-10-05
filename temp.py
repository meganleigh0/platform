from graphviz import Digraph

dot = Digraph(comment='The JSMC Production Process')

dot.node('A', 'Pre-Production')
dot.node('B', 'Initial Preparation')
dot.node('C', 'Fabrication')
dot.node('D', 'Assembly Line')
dot.node('E', 'Testing Phase')
dot.node('F', 'Final Delivery')

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF'])

# For Initial Preparation
dot.node('BA', 'Shot Blasting')
dot.node('BB', 'Painting and De-Masking')
dot.edges(['BA', 'BB'])  # Corrected this line

# For Fabrication
dot.node('CA', 'Cutting Operations')
dot.node('CB', 'Welding Operations')
dot.edges(['CA', 'CB'])  # And this line

# For Assembly Line
dot.node('DA', 'Hull Assembly')
dot.node('DB', 'Turret Assembly')
dot.node('DC', 'Final Assembly')
dot.edges(['DA', 'DB', 'DC'])  # And this line

# For Testing Phase
dot.node('EA', 'QA & Inspection')
dot.node('EB', 'Road Testing')
dot.node('EC', 'Final Acceptance Testing')
dot.edges(['EA', 'EB', 'EC'])  # And this line

dot.render('jsmc_process.gv', view=True)  # Output: jsmc_process.gv.pdf

