from graphviz import Digraph

dot = Digraph(comment='The JSMC Production Process', format='png')
dot.attr(rankdir='TB', size='10,10')

# Main Process Nodes with different shapes and colors
dot.node('A', 'Pre-Production', shape='ellipse', color='black', style='filled', fillcolor='lightyellow')
dot.node('B', 'Initial Preparation', shape='box', color='black', style='filled', fillcolor='lightpink')
dot.node('C', 'Fabrication', shape='box', color='black', style='filled', fillcolor='lightcyan')
dot.node('D', 'Assembly Line', shape='box', color='black', style='filled', fillcolor='lightcoral')
dot.node('E', 'Testing Phase', shape='ellipse', color='black', style='filled', fillcolor='lightgreen')
dot.node('F', 'Final Delivery', shape='ellipse', color='black', style='filled', fillcolor='lightgray')

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF'])

# Initial Preparation Sub-Nodes
dot.node('BA', 'Shot Blasting\n- Rust removal from hulls & turrets', shape='parallelogram', color='black')
dot.node('BB', 'Painting & De-Masking', shape='parallelogram', color='black')
dot.edges([('B', 'BA'), ('B', 'BB')])

# Fabrication Sub-Nodes
dot.node('CA', 'Cutting Operations\n- Laser, plasma, water jet cutting\n- Titanium alloy sheet cutting', shape='rectangle', color='black')
dot.node('CB', 'Welding Operations\n- Robotic & friction stir welding\n- Vehicle component fabrication', shape='rectangle', color='black')
dot.edges([('C', 'CA'), ('C', 'CB')])

# Assembly Line Sub-Nodes
dot.node('DA', 'Hull Assembly\n- Internal equipment & systems installation\n- Suspension components installation', shape='rectangle', color='black')
dot.node('DB', 'Turret Assembly\n- Cannon mounting & recoil testing\n- Ammo doors & component addition', shape='rectangle', color='black')
dot.edges([('D', 'DA'), ('D', 'DB')])
dot.node('DC', 'Final Assembly\n- Turret & hull marriage\n- Armor, skirting, final adjustments', shape='rectangle', color='black')
dot.edges([('DA', 'DC'), ('DB', 'DC')])

# Testing Phase Sub-Nodes
dot.node('EA', 'QA & Inspection\n- Multiple component inspections\n- Fire control systems calibration', shape='rectangle', color='black', style='filled', fillcolor='white')
dot.node('EB', 'Road Testing\n- Evaluation track road tests\n- Performance & tolerance tests', shape='rectangle', color='black', style='filled', fillcolor='white')
dot.node('EC', 'Final Acceptance Testing\n- GDLS & DCMA inspection\n- 1,200 item inspection process', shape='rectangle', color='black', style='filled', fillcolor='white')
dot.edges([('E', 'EA'), ('E', 'EB'), ('E', 'EC')])

# Render the Graph
dot.render('jsmc_process', view=True)
