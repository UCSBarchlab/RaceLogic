""" 
    Python 2.7 

    In Race Logic, a range of magnitudes can be encoded on a single wire with 
    a single edge (0 to 1 convention). Smaller delays in rise time encode 
    smaller magnitudes, while larger magnitudes are encoded as longer delays.

    Race logic's temporal coding base operations consists of four primary 
    functions: MAX, MIN, ADD-CONSTANT, and INHIBIT. 
    
    A PyRTL implementation of these 4 primitive Race Logic operators follows.

    Reference:
    G. Tzimpragos, A. Madhavan, D. Vasudevan, D. Strukov, and T. Sherwood, 
    "Boosted Race Trees for Low Energy Classification", in the 24th International 
    Conference on Architectural Support for Programming Languages and Operating 
    Systems (ASPLOS), Providence, RI, 2019.

    More about PyRTL: https://pyrtl.readthedocs.io/
"""

import pyrtl

def inhibit_rl(i, j):
    """
        The INHIBIT function has two inputs: an inhibiting signal i
        and a data signal j (that gets inhibited). If the inhibiting 
        signal arrives first, the output is prevented from ever going 
        high, which corresponds to inf in the race logic world. On 
        the other hand, if the data signal arrives before or at the 
        same time as the inhibiting signal, the former is allowed 
        to pass through unchanged. In other words, the inhibiting
        input acts as a gate that only allows an earlier arriving 
        or coincident data signal to pass.

        Inputs: 2 1-bit WireVectors
        Output: a 1-bit WireVector
    """
    i_before_j = pyrtl.Register(bitwidth = 1)
    i_before_j.next <<= (i & ~j) | i_before_j
    o = j & ~i_before_j
    return o

def max_rl(din):
    """
        A MAX function should "go high" only when all of
        its inputs have arrived. Thus, AND gates are 
        used for its implementation.

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
        A MIN function should "go high" when any of its 
        inputs arrives. Thus, OR gates are all that is 
        needed for its implementation.
        
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
        Since the arrival time of the rising edge is what encodes 
        information, delaying the 0 to 1 transition by a fixed 
        amount of time is equivalent to constant addition. Delaying 
        a race logic-encoded input can be performed with the use of
        a shift-register.

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
