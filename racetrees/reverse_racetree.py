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
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'base'))
from racelogic_primitives import *

### Basic building blocks ###

def fixed_inp_node(labels, attribute, c):
    """
        The values of input labels are known a priori.
    """
    controlling_inp = add_const_rl(din=attribute, k=c)
    inh_o = inhibit_rl(controlling_inp, labels[0])
    node_o = min_rl([inh_o, labels[1]])
    return node_o

def variable_inp_node(labels, min_label, attribute, c):
    """
        The values of input labels are not known a priori.
    """
    controlling_inp = add_const_rl(din=attribute, k=c)
    inh_o = inhibit_rl(controlling_inp, min_label)
    node_o = min_rl([max_rl([inh_o, labels[0]]), labels[1]])
    return node_o 
