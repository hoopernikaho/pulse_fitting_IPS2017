import numpy as np
import matplotlib.pyplot as plt

def hist(data,bins=400,lims=None, label='', Plot=True, alpha=.5):
    """Creates and Plots numpy histogram, removing the last bin""" 
    y, binEdges = data[:,0], data[:,1]
    if Plot:
        y_err = np.sqrt(y)
        width = binEdges[1]-binEdges[0]
        plt.bar(binEdges,y,yerr=y_err,alpha=alpha, width=width, label=label)
        plt.xlim(lims)
    return y, binEdges

data = np.loadtxt('/workspace/projects/TES/analysis/20170126_TES5_n012_distinguishibility_20MHz_tau_vs_offset_results/area_histogram/area_histogram_height_th_75e-4.txt')
plt.figure()
hist(data,bins=10)
plt.xlabel('Pulse Integral a.u.')
plt.ylabel('Number of Pulses')
plt.ylim([0,140])
plt.savefig('area_histo.eps')
plt.show()



