# D'Hondt Calculator

A Python implementation of the D'Hondt method for seat allocation in proportional representation electoral systems.

## Description

The D'Hondt method is a highest averages method for allocating seats in parliamentary systems. This calculator allows you to input election results and automatically calculates how seats should be distributed among parties according to the D'Hondt formula.

## How It Works

The D'Hondt method works by:
1. Dividing each party's vote total by 1, 2, 3, etc.
2. Allocating seats one by one to the party with the highest quotient
3. Repeating until all seats are allocated
