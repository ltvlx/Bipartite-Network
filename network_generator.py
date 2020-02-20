import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import codecs



def generate_network(N, Mc, probs, invert=False):
    """
    A small model of generating a directed bipartite network.
    Warning! The procedure has no fool proof.
    If the input parameters are such that the given number of edges is not achievable, 
        the program can crash or go into an infinite loop.

    input:
        N, int -- number of nodes in a network
        Mc, float -- percentage of non-zero elements in adjacency matrix, excluding diagonal
        probs, list[float] -- probablilities to create an edge between two nodes
        invert, bool -- key to invert the behavior by removing edges instead of adding
    output:
        send, list[int] -- list of sender node indexes 
        reci, list[int] -- list of reciever node indexes
        edges, list[(int, int)] -- list of edges as tuples of indexes

    First, N nodes are generated with an equal probability to be assigned 
        to one of the types: senders (s) and recievers (r).
    Second, based on the given probabilities, M edges are generated between those nodes, M = Mc * N * (N - 1).
        probs = [p_sr, p_ss, p_rr, p_rs]
    There are 4 possible edge types: 
        sr connects a random node of type (s) to a random node of type (r),
        ss connects a random node of type (s) to a random node of type (s),
        rr connects a random node of type (r) to a random node of type (r),
        rs connects a random node of type (r) to a random node of type (s).
    Self-loops, as well as repeating edges are not allowed.
    """
    assert(np.all(probs >= 0.0))
    assert(0.0 < Mc < 1.0)


    send = []
    reci = []
    for i in range(N):
        if np.random.random() < 0.5:
            send.append(i)
        else:
            reci.append(i)

    edges = set()
    while len(edges) < Mc * N * (N - 1):
        e_type = np.random.choice(['sr', 'ss', 'rr', 'rs'], p=probs)

        if e_type == 'sr':
            a = np.random.choice(send, 1)[0]
            b = np.random.choice(reci, 1)[0]
        elif e_type == 'ss':
            a = np.random.choice(send, 1)[0]
            b = np.random.choice(send, 1)[0]
        elif e_type == 'rr':
            a = np.random.choice(reci, 1)[0]
            b = np.random.choice(reci, 1)[0]
        elif e_type == 'rs':
            a = np.random.choice(reci, 1)[0]
            b = np.random.choice(send, 1)[0]

        if a != b:
            edges.add((a,b))
    
    if key_invert:
        all_edges = set([(a, b) for a in range(N) for b in range(N) if a != b])
        edges = all_edges - edges

    return send, reci, list(edges)


def draw_nw(send, reci, edges, path, i_seed):
    title = path[path.find('N='):]
    title = title.replace('-Mc=', ', Mc=')
    title = title.replace('-p=', ', p=[')
    if title.find('-inv') != -1:
        title = title.replace('-inv/', ']; inv')
    else:
        title = title.replace('/', ']')
    title = title.replace('_', ', ')

    G = nx.DiGraph()
    G.add_nodes_from(send + reci)
    G.add_edges_from(edges)
    pos = nx.circular_layout(G)
    # pos = nx.bipartite_layout(G, send)

    fig, ax = plt.subplots(figsize=(6, 6))

    nx.draw_networkx_nodes(G, pos, nodelist=send, node_color = 'C1', edgecolors = '#5c5c5c', linewidths = 0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=reci, node_color = 'C0', edgecolors = '#5c5c5c', linewidths = 0.5)
    nx.draw_networkx_labels(G, pos)

    nx.draw_networkx_edges(G, pos, style='solid', width=1.5, alpha=0.6)
    plt.title(title)

    plt.grid(alpha = 0.4, linestyle = '--', linewidth = 0.2, color = 'black')
    plt.axis('off')
    plt.savefig(path + f'seed={i_seed}.png', dpi=400, bbox_inches = 'tight', pad_inches=0.1)
    plt.close()
    # plt.show()




N = 15
Mc = 0.2
probs = [1, 49, 49, 1]   # sr, ss, rr, rs
probs = [49, 1, 1, 49]   # sr, ss, rr, rs
probs = [97, 1, 1, 1]   # sr, ss, rr, rs
probs = np.array(probs) / np.sum(probs)
key_invert = False

s_p = "_".join('%.2f'%x for x in probs)
s_inv = '-inv' if key_invert else ''
# path = f'N={N}-Mc={Mc:.2f}-{probs[0]:.2f}_{probs[1]:.2f}_{probs[2]:.2f}_{probs[3]:.2f}{s_inv}/'
path = f'N={N}-Mc={Mc:.2f}-p={s_p}{s_inv}/'
print(path)
if not os.path.exists(path):
    os.makedirs(path)


for i_seed in range(100):
    print(i_seed, end=', ', flush=True)
    np.random.seed(i_seed)
    
    send, reci, edges = generate_network(N, Mc, probs)

    if i_seed == 0:
        draw_nw(send, reci, edges, path, i_seed)

    with codecs.open(path + 'seed={:02d}.edges'.format(i_seed), 'w') as fout:
        for i, j in edges:
            fout.write('{}\t{}\t1\n'.format(i+1, j+1))
    




