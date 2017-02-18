import numpy as np
import matplotlib.pyplot as plt

def hist(data,bins=400,lims=None, label='', Plot=True, alpha=.5):
    """Creates and Plots numpy histogram, removing the last bin""" 
    y, binEdges = np.histogram(data,bins,range=(lims))
    if Plot:
        y_err = np.sqrt(y)
        step = binEdges[1]-binEdges[0]
        bins = binEdges[:-1]+step/2
        plt.bar(bins,y,yerr=y_err,alpha=alpha, width=step, label=label,align='center')
        plt.xlim(lims)
    return y, bins
heights = np.loadtxt('heights_single_diode_pulse.dat')
plt.figure()
freq, bins = hist(heights*1e3)
plt.xlabel('Pulse Amplitudes (mV)')
plt.ylabel('counts')
plt.vlines(7.5, np.min(freq), np.max(freq), linestyles='dashed')
plt.text(7.5, np.max(freq), 'threshold')
plt.savefig('height_distribution.eps')

plt.show()