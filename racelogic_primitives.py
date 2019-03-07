""" 
    Python 2.7 

    Implementation of the 4 primitive Race Logic operators in PyRTL.

    In Race Logic, a range of magnitudes can be encoded on a single wire with 
    a single edge (0->1 convention). Smaller delays in rise time encode 
    smaller magnitudes, while larger magnitudes are encoded as longer delays. 

    Reference:
    G. Tzimpragos, A. Madhavan, D. Vasudevan, D. Strukov, and T. Sherwood, 
    "Boosted Race Trees for Low Energy Classification", in the 24th International 
    Conference on Architectural Support for Programming Languages and Operating 
    Systems (ASPLOS), Providence, RI, 2019.

    More about PyRTL: https://pyrtl.readthedocs.io/
"""

import pyrtl
from racelogic_sim_input_stimuli import race_testval

def inhibit_rl(i, j):
    """
        Inhibit operator, where i inhibits j.
        Inputs: 2 1-bit WireVectors
        Output: a 1-bit WireVector
    """
    i_before_j = pyrtl.Register(bitwidth = 1)
    i_before_j.next <<= (i & ~j) | i_before_j
    o = j & ~i_before_j
    return o

def max_rl(din):
    """
        MAX function implemented with AND gates.
        Input: a list of 1-bit WireVectors
        Output: a 1-bit WireVector
    """
    if len(din) == 1:
        dout = din[0]
    else:
        dout = din[0] & max_rl(din[1:])
    return dout

def min_rl(din):
    """
        MIN function implemented with OR gates.
        Input: a list of 1-bit WireVectors
        Output: a 1-bit WireVector
    """
    if len(din) == 1:
        dout = din[0]
    else:
        dout = din[0] | min_rl(din[1:])
    return dout

def add_const_rl(din, k):
    """
        ADD-CONSTANT function implemented with a shift-register.
        Input: a 1-bit WireVector, k: added constant
        Output: a 1-bit WireVector
    """
    if k == 0:
        return din
    else:
        sr = pyrtl.Register(bitwidth = k)
        if k == 1:
            sr.next <<= din
        else:
            sr.next <<= pyrtl.concat(sr[:-1], din)
        return sr[-1]

'''
### Testing ###

# List of input values
test_din = [5, 2, 4]

# Create input wirevectors and assign the corresponding race values to them 
sim_dict = {}
din_wv = []
for i, val in enumerate(test_din):
    locals()["din"+str(i)] = pyrtl.Input(bitwidth = 1, name = str("din%d"%i)) 
    sim_dict[str("din%d"%i)] = race_testval(val).next 
    din_wv.append(locals()["din"+str(i)])

# Create output wirevectors
inh_out_case0 = pyrtl.Output(bitwidth = 1, name = "inh(din1,din0)_out")
inh_out_case1 = pyrtl.Output(bitwidth = 1, name = "inh(din0,din1)_out")
max_out = pyrtl.Output(bitwidth = 1, name = "max_out")
min_out = pyrtl.Output(bitwidth = 1, name = "min_out")
add_const_out = pyrtl.Output(bitwidth = 1, name = "add_const_out")

# Call functions
inh_out_case0 <<= inhibit_rl(din1, din0) # controlling input: din1
inh_out_case1 <<= inhibit_rl(din0, din1) # controlling input: din0
max_out <<= max_rl(din_wv)
min_out <<= min_rl(din_wv)
add_const_out <<= add_const_rl(din0, 3) # add k=3

# Simulate  
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(10):
    sim.step({k: v() for k, v in sim_dict.items()})
sim_trace.render_trace()

exit(0)
'''
