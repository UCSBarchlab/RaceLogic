""" 
    Python 2.7 
    
    Simulate a Reverse Race Tree (paper's example).

    Labels policy: 
    The delay-coded label associated with a leaf should always be greater than 
    the thresholds of the nodes found on its path to the root (we cannot add 
    negative "numbers"). Moreover, the label values of a tree must on all occasions
    increment monotonically from right (all "False" branches) to left (all "True" 
    branches).

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
from reverse_racetree import *
from racelogic_primitives import *
from racelogic_sim_input_stimuli import race_testval


### Testing ###

# Labels
label_vals = [3, 4, 5, 6]
sim_dict = {}
labels_wv = []
for i, val in enumerate(label_vals):
    locals()["label"+str(len(label_vals)-i-1)] = pyrtl.Input(bitwidth = 1, name = str("label%d"%(len(label_vals)-i-1))) 
    sim_dict[str("label%d"%(len(label_vals)-i-1))] = race_testval(val).next 
    labels_wv.append(locals()["label"+str(len(label_vals)-i-1)])

# Attributes
x = pyrtl.Input(bitwidth = 1, name = 'x')
y = pyrtl.Input(bitwidth = 1, name = 'y')
x_val, y_val = 2, 3
sim_dict["x"] = race_testval(x_val).next
sim_dict["y"] = race_testval(y_val).next

# Decision/Output
out = pyrtl.Output(bitwidth = 1, name = 'out')

# Paper's example reverse tree
fixed_inp_node_out_right = pyrtl.WireVector(bitwidth = 1, name = 'fixed_inp_node_out_right')
fixed_inp_node_out_left = pyrtl.WireVector(bitwidth = 1, name = 'fixed_inp_node_out_left')
fixed_inp_node_out_right <<= fixed_inp_node(labels_wv[0:2], y, 1)
fixed_inp_node_out_left <<= fixed_inp_node(labels_wv[2:4], x, 3)
out <<= variable_inp_node([fixed_inp_node_out_right, fixed_inp_node_out_left], labels_wv[0], x, 0) 

# Simulate 
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(10):
    sim.step({k: v() for k, v in sim_dict.items()})
sim_trace.render_trace()

exit(0)
