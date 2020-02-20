# Bipartite Network
A small model of generating a directed bipartite network.
Each of N nodes has a 50% to be assigned to a class S (senders) or R (recievers).
Then, M = M<sub>c</sub>\*N\*(N-1) edges between those nodes are generated using 4 probabilities p=[p<sub>sr</sub>, p<sub>ss</sub>, p<sub>rr</sub>, p<sub>rs</sub>]. p<sub>sr</sub> is the probability that a new edge would connect 2 random nodes of class S and R, p<sub>ss</sub> - of class S and S, and so on.  
Self-loops, as well as repeating edges are not allowed.

Warning! The procedure has no fool proof. If the input parameters are such that the given number of edges is not achievable, the program can crash or go into an infinite loop.

Input parameters:  
- N - number of nodes in a network
- Mc - percentage of non-zero elements in adjacency matrix, excluding diagonal
- probs - probablilities to create an edge between two nodes



