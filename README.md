# Chinampas
Code for the paper https://arxiv.org/abs/2103.15265


A chinampa of arbitrary profit looks like the figure below.

![standart](https://user-images.githubusercontent.com/18435221/112927159-8c8d2100-90e2-11eb-93a0-69e93edf529b.png)

Zooming out, we see chains of isoceles right triangles of different size but all looking at the same direction, stacked into each other.

Zooming in, we see a model of neural activations, or cellular automata following rule 192.

This repository contains [a pdf](R7.pdf) and the mathematica [code](Computation_of_R7.nb) with our calculations to determine the generating series of the triangular sequence R7.

A Jupyter notebook explaining the paper is located at  [Notebook](Chinampas.ipynb). A Mathematica notebook explaining the calculations is located at [mathematica notebook](Introduction.nb) (or the pdf [introduction](introduction.pdf) ). 

### Code:
How to reproduce a cascade efficiently? 
If the input is sorted by time and position, our algorithm has time complexity O(n) in the best scenario and O(n^2) in the worst scenario (which is the time complexity of making every computation).

Will a vertex be activated at a particular time given a certain input?
We wrote a function that answers this questions efficiently. 
[Luke's code].

Here is a [python program](main.py) to find those chinampas of profit 0.

### Funding 
This project has received funding from the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (No. 2020R1C1C1A0100826).
