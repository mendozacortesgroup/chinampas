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
[chinampas](src/chinampas.py).
Example for chinampas in a line:
"""
import chinampas as ch
activations = [[0,0],[1,0],[4,4],[5,4],[6,4],[7,5]]
chain = ch.Chain_Chinampa(activations)
print(f" Will vertex 7 at time 6 be activated?  {chain.will_vertex_be_activated(7,6)} ")
print(f"list of pyramids in the chinampa: {[(pyramid.lP,pyramid.rP,pyramid.time) for pyramid in chain.pyramids]}")
"""
Example for chinampas in a tree:

"""
import chinampas as ch
tree = ch.Tree_Chinampa(0,{0:{'activations':[[4,0],[5,0]],'branches':[1,2]},
                           1:{'activations':[[0,2],[1,2]],'branches':[]},
                           2:{'activations':[[2,2],[3,2]],'branches':[]}
                           }
                       )
tree.will_vertex_be_activated(4,3) #The node index is global i.e, node 0 is in branch 1, node 2 in branch 2, etc. -Luke
                              
"""

Here is a [python program](main.py) to find those chinampas of profit 0.

### Funding 
This project has received funding from the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (No. 2020R1C1C1A0100826).
