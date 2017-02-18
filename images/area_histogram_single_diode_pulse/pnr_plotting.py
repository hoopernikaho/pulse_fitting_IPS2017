import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 20})
def hist(data,bins=400,lims=None, label='', Plot=True, alpha=.5):
    """Creates and Plots numpy histogram, removing the last bin""" 
    y, binEdges = np.histogram(data,bins,range=(lims))
    if Plot:
        y_err = np.sqrt(y)
        step = binEdges[1]-binEdges[0]
        bins = binEdges[:-1]+step/2
        plt.bar(bins,y,yerr=y_err,alpha=alpha, width=step, label=label)
        plt.xlim(lims)
    return y, bins

data = np.loadtxt('areas_single_diode_pulse.dat')
plt.figure()
plt.tight_layout
# plt.hist(data,200)
hist(data,bins=200,lims=[0,5])
plt.xlabel('Pulse Area')
plt.ylabel('Number of Pulses')
plt.ylim([0,650])
plt.savefig('area_histo.pdf')
plt.show()



