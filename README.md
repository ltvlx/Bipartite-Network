# Bipartite Network
A small model of generating a directed bipartite network.  
Each of N nodes has a 50% to be assigned to one of the classes A or B.  
Then, M = M<sub>c</sub>\*N\*(N-1) edges between those nodes are generated using 4 probabilities p=[p<sub>aa</sub>, p<sub>ab</sub>, p<sub>ba</sub>, p<sub>bb</sub>].  
p<sub>aa</sub> is the probability that a new edge would connect a random node of class A to another random node of class A,  
p<sub>ab</sub> - a random node of class A would connect to a random node from class B, and so on.  
Self-loops, as well as multiple edges are not allowed.

Warning! The procedure has no fool proof. If the input parameters are such that the given number of edges is not achievable, the program can crash or go into an infinite loop.

Input parameters:  
- N - number of nodes in a network
- Mc - percentage of non-zero elements in adjacency matrix, excluding diagonal
- probs - probablilities to create an edge between two nodes



