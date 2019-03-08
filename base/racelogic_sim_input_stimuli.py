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
