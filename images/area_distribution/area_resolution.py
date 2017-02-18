import matplotlib
matplotlib.rcParams.update({'font.size': 20})
import numpy as np
import matplotlib.pyplot as plt
from thres_poiss import *


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

area_abs = np.loadtxt('absolute_area.dat')
area_win = np.loadtxt('windowed_area.dat')

"""windowed areas histogram and fit"""
plt.figure()
plt.tight_layout
freq, bins = np.histogram(area_win,100, range=(0,1.4))
# print peaks([freq[1:], bins[1:]], min_peak_sep=0.2, threshold=.2)
plt.hist(area_win,100,range=(0,1.4))
plt.ylim([0,450])
result = gauss_fit_interp([freq[1:], bins[1:]], min_peak_sep=0.2, threshold=.2)
# print result.eval_components()['g0_']
print len(result.best_fit)
print len(bins)

min_overlaps=[min_overlap_stats(result.values['g{}_center'.format(k)],
	result.values['g{}_center'.format(k+1)],
	result.values['g{}_sigma'.format(k)],
	result.values['g{}_sigma'.format(k+1)]) for k in np.arange(1)][0]
# print min_overlaps
print ('threshold between n = 1, n = 2: {}\n prob n=2 photons identified as n=1: {}\n prob n=1 photons identified as n=2: {}'.format(min_overlaps[0],
	min_overlaps[1],
	min_overlaps[2]))

plt.text(0.05, 200, 'n=0')
plt.text(0.65, 200, 'n=1')
plt.text(1, 100, 'n=2',ha='center')
plt.xlabel('Isolated Pulse Area')
plt.ylabel('counts')
plt.savefig('area_windowed_histo.eps', bbox_inches='tight')

"""absolute areas histogram"""
plt.figure()
plt.hist(area_abs, 100, range=(0.6,2))
plt.xlim([.6,2])
plt.text(.85, 925, 'n=0', ha='center')
plt.text(1.25, 500, 'n=1', ha='center')
plt.text(1.6, 200, 'n=2', ha='center')
plt.xlabel('Pulse Area')
plt.ylabel('counts')
plt.tight_layout
plt.savefig('area_abs_histo.eps', bbox_inches='tight')

# plt.show()