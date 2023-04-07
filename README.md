# Piston Balancing

A practical problem in automobile mechanics.

## Problem Statement

In a combustion motor, it's best if the masses of the different piston assemblies are roughly the same.

Each piston assembly consist of three components: 
* Piston
* Connecting Rod
* Pin

A car motor may have somewhere between 4 and 16 cylinders (for piston assemblies). Call this n.

Given [n] sets of (pin, rod, piston): How can we mix and match these components __such that the variance (in grams) between assembled sets is minimized?__

One might alternatively seek to minimize the difference between the heaviest and the lightest assembly.

## Methods

A brute-force approach is demonstrated in [Pistons.ipynb](Pistons.ipynb).

The nasty nested for-loop does not scale beyond 4 cylinders on a consumer laptop.

In [pistons_multithreaded.py](pistons_multithreaded.py), the same ugly approach is thrown at more cores. It took me 17 minutes to solve for 6 cylinders on an 8-core macbook air.

## RFP

Now it's your turn to find a smarter approach to this problem. How can this be computed for a 16-cylinder engine?