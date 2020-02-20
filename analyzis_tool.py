import matplotlib.pyplot as plt
import numpy as np
import codecs
from subprocess import run
import os
import networkx as nx


np.set_printoptions(precision=2, suppress=True)



def run_mfinder(N_nw):
    for i in range(N_nw):
        fname = 'seed={:02d}.edges'.format(i)
        if os.path.isfile(fname):
            run('mfinder1.2.exe ' + fname)


def read_motif_data(N_nw):
    id2x = {6: 0,  36: 1, 12: 2, 74: 3, 14: 4, 78: 5, 38: 6, 98: 7, 108: 8, 46: 9, 102: 10, 110: 11, 238: 12}

    # y_data = np.zeros((N, 13))
    y_data = [[] for i in range(13)]
    # for i_seq, i_real in nw_dict.items():
    for i_seed in range(N_nw):
        fname = 'seed={:02d}.e_OUT.txt'.format(i_seed)
        with codecs.open(fname, 'r') as fin:
            start = 'ID		STATS		ZSCORE	PVAL	[MILI]'
            kk = len(start)
            
            for line in fin:
                if line[:kk] == start:
                    break
            else:
                print("Warning! no motifs information found in the following file:")
                print(fname, flush=True)
                return
            
            motif_z = {}
            for _ in range(13):
                line = fin.readline()
                vals = line.split()
                motif_id = int(vals[0])
                if vals[3] != '888888':
                    motif_z[id2x[motif_id]] = float(vals[3])
                line = fin.readline()

            # Normalization
            if motif_z != {}:
                norm = np.sqrt(np.sum(np.array(list(motif_z.values()))**2))
            else:
                norm = 1

            for key, val in motif_z.items():
                motif_z[key] = val / norm
                y_data[key].append(val / norm)

    x = [2*i for i in range(13)]
    y = []
    for row in y_data:
        y.append(np.array(row))
    return x, y



def get_pos(k):
    dy = 0.87
    dx = 2.0
    h = 0.09

    pos = {'A': [0.0, h], 'B': [-0.5, 0.0], 'C': [0.5, 0.0], 'label': [0.0, -h]}

    for key in pos:
        pos[key][0] += dx * k
        pos[key][1] -= dy
    
    return pos
    


def plot_motif_scores(N_nw, title):
    # Plot motif images at the bottom
    motifs_dict = {
        6: [('A','B'), ('A','C')],
        36: [('A','C'), ('B','C')],
        12: [('A','B'), ('B','C')],
        74: [('A','B'), ('B','C'), ('C','B')],
        14: [('A','B'), ('B','C'), ('B','A')],
        78: [('A','B'), ('B','C'), ('B','A'), ('C','B')],
        38: [('A','B'), ('B','C'), ('A', 'C')],
        98: [('A','B'), ('B','C'), ('C', 'A')],
        108: [('A','B'), ('A','C'), ('B','C'), ('C','B')],
        46: [('A','B'), ('B','A'), ('A','C'), ('B','C')],
        102: [('A','B'), ('B','C'), ('C', 'A'), ('A','C')],
        110: [('A','B'), ('B','C'), ('C', 'A'), ('A','C'), ('C', 'B')],
        238: [('A','B'), ('B','A'), ('B','C'), ('C', 'B'), ('A','C'), ('C', 'A')]
    }

    fig, ax = plt.subplots(figsize=(9, 6))
    k = 0
    # for m_id in sorted(motifs_dict.keys()):
    for i in range(13):
        m_id = [6, 36, 12, 74, 14, 78, 38, 98, 108, 46, 102, 110, 238][i]
        
        axis = ax
        e_list = motifs_dict[m_id]
        m = nx.DiGraph()
        m.add_nodes_from(['A', 'B', 'C'])
        m.add_edges_from(e_list)
        pos = get_pos(k)
        nx.draw_networkx_nodes( m, pos, node_size=40, node_color=['C4', 'C1', 'C2'], ax=axis)
        nx.draw_networkx_edges( m, pos, node_size=40, width=1.0, arrowsize = 8, ax=axis)
        # nx.draw_networkx_labels(m, pos, font_size=8, ax=axis)

        axis.text(pos['label'][0], pos['label'][1], '%d'%(i+1), horizontalalignment='center')
        k += 1


    x, y = read_motif_data(N_nw)
    means = []
    for kk in range(13):
        print(kk, y[kk])
        # Violin plot
        if y[kk].size != 0:
            parts = ax.violinplot(y[kk], [kk*2], points=60, widths=0.9, showmeans=False, showextrema=False, bw_method=0.5)
            for pc in parts['bodies']:
                pc.set_facecolor('C0')
                # pc.set_edgecolor('black')
                pc.set_alpha(0.4)

            # Mean + error bars
            y_s = np.std(y[kk])
            y_m = np.mean(y[kk])
            means.append(y_m)
            ax.errorbar([kk*2], y_m, yerr=y_s, fmt='o', color='#4764a8', capsize=3.0)
        else:
            means.append(0.0)

    ax.plot(x, means, '-', lw=0.7, color='#4764a8')


    ax.plot([-1.0, 25.0], [0.0, 0.0], '--', lw=0.5, color='black', zorder=0, alpha=0.5)
    ax.set_ylabel('z-score, normalized')

    # ax.text(0.90, 0.95, '{}/{}'.format(len(nw_dict), N_nw), transform=ax.transAxes)

    ax.set_xticks(np.arange(0,25,2))
    ax.set_xticklabels('')

    y_range = np.arange(-0.6, 1, 0.2)
    ax.set_yticks(y_range)
    ax.set_yticklabels(['%.1f'%val for val in y_range])

    ax.tick_params(bottom=False, left=True, labelleft=True, labelbottom=False)
    
    plt.title(title)

    ax.set_xlim((-1.0, 25.0))
    ax.set_ylim((-1.0, 0.8))
    # ax.set_ylim((-0.5, 0.5))
    ax.grid(alpha = 0.6, linestyle = '--', linewidth = 0.2, color = 'black')


    plt.savefig('motifs-no88.png', dpi=400, bbox_inches = 'tight')
    plt.show()






N_nw = 100

dirpath = os.getcwd()
title = dirpath[dirpath.find('N='):]
title = title.replace('-Mc=', ', Mc=')
title = title.replace('-p=', ', p=[')
if title.find('-inv') != -1:
    title = title.replace('-inv', ']; inv')
else:
    title += ']'
title = title.replace('_', ', ')

# run_mfinder(N_nw)
plot_motif_scores(N_nw, title)

