""" 
    Python 2.7 

    Simulate race logic's four primary functions: 
    MAX, MIN, ADD-CONSTANT, and INHIBIT.  
"""

import pyrtl
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'base'))
from racelogic_primitives import *
from racelogic_sim_input_stimuli import race_testval

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
