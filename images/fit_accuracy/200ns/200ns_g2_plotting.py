import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 20})
def hist(data,bins=200,lims=None, label='', Plot=True, alpha=.5):
    """Creates and Plots numpy histogram, removing the last bin""" 
    y, binEdges = np.histogram(data,bins,range=(lims))
    if Plot:
        y_err = np.sqrt(y)
        step = binEdges[1]-binEdges[0]
        bins = binEdges[:-1]+step/2
        plt.bar(bins,y,yerr=y_err,alpha=alpha, width=step, label=label)
        plt.xlim(lims)
    return y, bins

data=np.array(np.genfromtxt('200ns_separation_offset_amplitude_data.txt',names=True))
tau = np.abs(data['one_x_offsets']-data['two_x_offsets'])*1e9
plt.figure()
hist(tau,lims=[0,400])
plt.ylim(0,100)
plt.xlabel('time (ns)')
plt.ylabel('counts')

# plt.semilogy()
plt.savefig('200ns_g2.pdf')


