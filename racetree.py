""" 
    Python 2.7 
    
    Example Race Tree.
    
    More about PyRTL: https://pyrtl.readthedocs.io/
"""

import pyrtl
import math
from racelogic_primitives import *
from racelogic_sim_input_stimuli import *

class RaceTree(attributes, tree_nodes):
    
    def __init__(self):
        self.inp_res = inp_res
        self.attributes = attributes
        self.tree_nodes = tree_nodes
        return 

    def decoder(self, din):
        dec_ins = [[None for x in range(depth)] for y in range(2**depth)]
        step = 2**depth
        idx = 0
        for i in range(depth):
            for j in range(2**depth):
                if (j%step == 0):
                    idx += 1
                if (j//(step/2))%2:
                    dec_ins[j][i] = ~ din[idx-1]
                else:
                    dec_ins[j][i] = din[idx-1]
            step = step/2
        addr_1hot = [pyrtl.Const("1'b1") for y in range(2**depth)]
        for j in range(2**depth):
            for i in range(depth):
                addr_1hot[j] = addr_1hot[j] & dec_ins[j][i]
        addr = onehot2bin(addr_1hot)
        return addr

    def tree(self):
        # create a local copy of the input feature data (tree's attributes)
        a = data_buffer(self.attributes)
        # create delay-coded thresholds
        t = shift_reg(din = pyrtl.Const("1'b1"), n = 2**self.inp_res - 1)
        # connect attributes and thresholds to the inhibits implementing tree's nodes
        tree_inhs_o = [inhibit_rl(t[self.tree_nodes[i][0]], a[self.tree_nodes[i][1]]) for i in range(len(self.tree_nodes))]
        # decode
        decision = self.decoder(tree_inhs_o)
        valid_out = t[-1]
        return decision, valid_out


### Auxiliary "functions" ###

def shift_reg(din, n):
    """
        Use a shift register to create delay-coded thresholds.
    """
    sr = pyrtl.Register(bitwidth = n)
    sr.next <<= pyrtl.concat(sr[:-1], din)
    return sr

def data_buffer(din):
    """
        Create a data buffer.
    """
    dt_buffer = pyrtl.Register(bitwidth = len(din))
    dt_buffer.next <<= din
    return dt_buffer


### Testing ###

# Build
x = pyrtl.Input(bitwidth = 1, name = 'x')
y = pyrtl.Input(bitwidth = 1, name = 'y')
o = pyrtl.Input(bitwidth = , name= 'o')

tree_depth = 2
inp_res = 4
attributes = pyrtl.concat_list([x,y])
tree_nodes = [[2, 0], [1, 0], [1, 1]] # [threshold, attribute_index]

RT = RaceTree(attributes, tree_nodes)

# Simulate
k, l = race_testval(2), race_testval(3)
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(2**inp_res):
    sim.step({
        'x' : k.next(),        
        'y' : l.next()
        })
sim_trace.render_trace()

exit(0)
