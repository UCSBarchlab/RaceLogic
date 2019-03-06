""" 
    Python 2.7 

    Simulate input stimuli.

    More about PyRTL: https://pyrtl.readthedocs.io/
"""

import pyrtl

def race_testval(x):
    """
        Generator returning a delay-encoded value for x.
    """
    if x is None:
        while True:
            yield 0
    else:
        for i in range(x):
            yield 0
        while True:
            yield 1

'''
### Testing ###

# List of input values
ft_values_in = [5, 2,4]

# Create input wirevectors and assign the corresponding race values to them 
sim_dict = {}
for i, val in enumerate(ft_values_in):
    locals()["din"+str(i)] = pyrtl.Input(bitwidth = 1, name = str("din%d"%i)) 
    sim_dict[str("din%d"%i)] = race_testval(val).next 

# Simulate  
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)
for cycle in range(10):
    sim.step({k: v() for k, v in sim_dict.items()})
sim_trace.render_trace()

exit(0)
'''
