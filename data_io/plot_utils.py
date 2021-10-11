import numpy as np

import matplotlib.pyplot as plt
import matplotlib        as mpl

def plot_3d_hits_double(hits, hits2, double = True, value='energy', coords = ['x', 'y', 'z'], cmap = mpl.cm.jet, value2 = 'E', coords2 = ['X', 'Y', 'Z'], opacity = 0.1, label1 = None, label2 = None):
    #Función para hacer plot de distintos hits de un mismo evento superponiéndose
    
    fig  = plt.figure(figsize=(15, 15), frameon=False)
    gs   = fig.add_gridspec(2, 40)
    ax   = fig.add_subplot(gs[0, 0:16], projection = '3d')
    axcb = fig.add_subplot(gs[0, 18])
    norm = mpl.colors.Normalize(vmin=hits.loc[:, value].min(), vmax=hits.loc[:, value].max())

    m    = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    colors = np.asarray(np.vectorize(m.to_rgba)(hits.loc[:, value]))
    colors = np.rollaxis(colors, 0, 2)

    ax.scatter(hits[coords[0]], hits[coords[1]], hits[coords[2]], c=colors, marker='o', label = label1)
    cb = mpl.colorbar.ColorbarBase(axcb, cmap=cmap, norm=norm, orientation='vertical')

    if double == True:
        
        norm2   = mpl.colors.Normalize(vmin=hits2.loc[:, value2].min(), vmax=hits2.loc[:, value2].max())

        m2      = mpl.cm.ScalarMappable(norm=norm2, cmap=cmap)

        colors2 = np.asarray(np.vectorize(m2.to_rgba)(hits2.loc[:, value2]))
        colors2 = np.rollaxis(colors2, 0, 2)

        ax.scatter(hits2[coords2[0]], hits2[coords2[1]], hits2[coords2[2]], c=colors2, marker='o', alpha = opacity, label = label2)
    
    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')
    ax.set_zlabel('Z ')
    cb.set_label (value)
    if label1 != None:
        ax.legend()

    plt.show()
