# Race Logic

When extremely low-energy processing is required, the choice of data representation makes a tremendous difference. Each representation (e.g. frequency domain, residue coded, log-scale) comes with a unique set of trade-offs -- some operations are easier in that domain while others are harder. The core idea behind Race Logic is to do computation through the purposeful manipulation of signal delays (either synchronously or asynchronously) rather than final logic levels. All signals are supposed to be 0 or 1 at all times. However, the time at which 0 to 1 transition happens encodes the value. Computations can then be based on the observation of the relative propagation times of signals injected into a configurable circuit. 

Race Logic's temporal coding base operations consists of four primary functions: MAX, MIN, ADD-CONSTANT, and INHIBIT. Together this set of operations allow us to deliberately engineer "race conditions" in a circuit to perform useful computation. The resulting systems use only one wire per operand (leading to both smaller area and capacitance) and at most one bit-flip per wire to perform the desired operation (resulting in less switching activity and dynamic power). While not all computations are amenable to such an encoding, those that are have the potential to operate with very little energy. 

In a nutshell, though application specific, a change of information representation allows problems to be reformulated in a way that can be performed both quickly and efficiently, and race logic does just that. On one hand, the temporal domain representation, which allows multiple values to be encoded on the same wire, coupled with simple digital primitives and a low logic depth, allow high speed. On the other hand, a single edge transition per computation running down a spatially laid out architecture allows for superior energy efficiency.

### Package Contents

In the package you should find the following directories:
* *base/*   PyRTL implementations of Race Logic's primary operations and other useful functions. 
* *racetrees/*    PyRTL implementations of the Flat and Reverse Race Trees presented in [1].
* *tests/*    A set of tests for all PyRTL-based Race Logic implementations.

### Example Usage

Install PyRTL (https://pyrtl.readthedocs.io/)

```sudo pip install pyrtl``` or ```pip install --user pyrtl```

then run example (Python 2.7)

```python tests/{test_name}```

### References:

[1] G. Tzimpragos, A. Madhavan, D. Vasudevan, D. Strukov, and T. Sherwood, "Boosted Race Trees for Low Energy Classification", in the 24th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS), Providence, RI, 2019. (Best Paper Award)

[2] A. Madhavan, T. Sherwood and D. Strukov, "Energy efficient computation with asynchronous races", in the 53rd Annual Design Automation Conference (DAC), New York, NY, 2016.

[3] A. Madhavan, T. Sherwood and D. Strukov, "Race Logic: Abusing Hardware Race Conditions to Perform Useful Computation", IEEE Micro: Micro's Top Picks from Computer Architecture Conferences, 2015.

[4] A. Madhavan, T. Sherwood and D. Strukov, "Race Logic: A hardware acceleration for dynamic programming algorithms", in the 41st International Symposium on Computer Architecture (ISCA), Minneapolis, MN, 2014.

### Other related work:

- G. Tzimpragos, D. Vasudevan, N. Tsiskaridze, G. Michelogiannakis, A. Madhavan, J. Volk, J. Shalf, and T. Sherwood, "A Computational Temporal Logic for Superconducting Accelerators", in the 25th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS), Lausanne, Switzerland, 2020. Github:https://github.com/UCSBarchlab/Superconducting-Temporal-Logic
- J. E. Smith, "Space-time algebra: a model for neocortical computation", in the 45th Annual International Symposium on Computer Architecture (ISCA), Los Angeles, CA, 2018.
- J. E. Smith, M. Martonosi, "Space-Time Computing with Temporal Neural Networks", Morgan & Claypool Publishers, 2017.


### Contact:

For general questions feel free to reach out to [Archlab @ UCSB](https://www.arch.cs.ucsb.edu/).

For immediate help with Race Logic and PyRTL, contact George (gtzimpragos@cs.ucsb.edu).
