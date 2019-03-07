""" 
    Python 2.7 
    
    Reverse Race Tree:
    Leaf labels can be thought of as packets that are routed through a "reverse
    tree" network. Some packets are discarded along the way, but the packet at
    the output has been routed unchanged. Externally, the packets are assigned
    values that are purely symbolic and contain no useful numerical content --
    in much the same way that numbers in sudoku are used symbolically, but
    not numerically. However, internal to the network, as part of the routing
    architecture, the packet values do take part in numerical operations.
    
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

    More about PyRTL: https://pyrtl.readthedocs.io/
"""

import pyrtl
from racelogic_primitives import *
from racelogic_sim_input_stimuli import race_testval

### Basic building blocks ###

def fixed_inp_node(labels, attribute, c):
    controlling_inp = add_const_rl(din=attribute, k=c)
    inh_o = inhibit_rl(controlling_inp, labels[0])
    node_o = min_rl([inh_o, labels[1]])
    return node_o

def variable_inp_node(labels, min_label, attribute, c):
    controlling_inp = add_const_rl(din=attribute, k=c)
    inh_o = inhibit_rl(controlling_inp, min_label)
    node_o = min_rl([max_rl([inh_o, labels[0]]), labels[1]])
    return node_o 

'''
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
o = pyrtl.Output(bitwidth = 1, name = 'o')

# Paper's example reverse tree
fixed_inp_node_out_right = pyrtl.WireVector(bitwidth = 1, name = 'fixed_inp_node_out_right')
fixed_inp_node_out_left = pyrtl.WireVector(bitwidth = 1, name = 'fixed_inp_node_out_left')
fixed_inp_node_out_right <<= fixed_inp_node(labels_wv[0:2], y, 1)
fixed_inp_node_out_left <<= fixed_inp_node(labels_wv[2:4], x, 3)
o <<= variable_inp_node([fixed_inp_node_out_right, fixed_inp_node_out_left], labels_wv[0], x, 0) 

# Simulate 
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(10):
    sim.step({k: v() for k, v in sim_dict.items()})
sim_trace.render_trace()

exit(0)
'''
