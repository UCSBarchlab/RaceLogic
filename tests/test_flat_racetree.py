""" 
    Python 2.7 
    
    Simulate a Flat Race Tree (paper's example).
   
    Reference: 
    G. Tzimpragos, A. Madhavan, D. Vasudevan, D. Strukov, and T. Sherwood, 
    "Boosted Race Trees for Low Energy Classification", in the 24th International 
    Conference on Architectural Support for Programming Languages and Operating 
    Systems (ASPLOS), Providence, RI, 2019.
"""

import pyrtl
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'base'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'racetrees'))
from flat_racetree import FlatRaceTree
from racelogic_sim_input_stimuli import race_testval


### Testing ###

inp_res = 4 # input resolution -- in this case we are using 4-bit inputs
tree_depth = 2 # depth of the tree

# Build
x = pyrtl.Input(bitwidth = 1, name = 'x')
y = pyrtl.Input(bitwidth = 1, name = 'y')
out_bin = pyrtl.Output(bitwidth = tree_depth, name = 'out_bin')
valid_out = pyrtl.Output(bitwidth = 1, name = 'valid_out')

attributes = pyrtl.concat_list([x,y]) # list of the tree's attributes
tree_nodes = [[2, 0], [1, 0], [1, 1]] # [threshold, attribute_index]

RT = FlatRaceTree(inp_res, tree_depth, attributes, tree_nodes)

tree_out = RT.tree()
out_bin <<= tree_out[0]
valid_out <<= tree_out[1]

# Simulate
k, l = race_testval(2), race_testval(3)
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(2**inp_res + 1):
    sim.step({
        'x' : k.next(),        
        'y' : l.next()
        })
sim_trace.render_trace(symbol_len=5, segment_size=1)

exit(0)
