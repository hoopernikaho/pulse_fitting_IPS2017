"""
g2 plotting with modelling for CW source.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 20})

g2 = np.load('/workspace/projects/TES/analysis/20161116_TES5_20MHz_bwl_diode_n012_height_optimised_results/taus_fit_using_edges_by_diff_hys_mcmc.npy')

def hist(data,numbins=400,lims=None, label='', plot=True, alpha=.5):
    """Creates and Plots numpy histogram, removing the last bin""" 
    y, binEdges = np.histogram(data,numbins,range=(lims))
    if plot:
        y_err = np.sqrt(y)
        step = binEdges[1]-binEdges[0]
        _bins = binEdges[:-1]+step/2
        plt.bar(_bins,y,yerr=y_err,alpha=alpha, width=step, label=label, align='center')
        # plt.errorbar(_bins,y,yerr=y_err)
        plt.xlim(lims)
    return y, _bins

def model(numdata, bins, lims, plot=False):
	"""
	Free running coherent state g2 (expected)
	    Fixed Trace length T of bins
	    g2 length g2_T of g2_bins
	"""
	g2_T = np.diff(lims)*1e-9 
	# 10000e-9
	g2_bins = bins
	# 20
	T = 10e-6 #trace length
	dT = g2_T/g2_bins #g2 scope / bins in g2 scope
	bins = T/dT #bins in a trace
	# nbar = lambda bins: 40e3/.47*.872*dT #APD rates/ APD eff / TES eff / trace length
	# poiss = lambda k, nbar: nbar**k*np.exp(-1*nbar)/math.factorial(k) 
	prob = lambda tau,bins: 2/bins**2*(T-tau)/(dT)
	taus = np.linspace(dT/2,g2_T-dT/2,g2_bins)#g2 scope, bins in g2 scope
	if plot:
		plt.plot(taus*1e9,prob(taus,bins)*numdata,'-', linewidth=4)
	return prob(taus,bins)*numdata

def redchisq(x,y,yerr,f):
	return np.sum(np.abs(np.abs(f-y)/yerr/(len(y)-2)))

if __name__ == '__main__':
	# numbins = 25
	# lims = [0,800] #units ns
	numbins = 40
	lims = [0,10000] #units ns

	plt.figure()
	y, bins = hist(np.abs(g2*1e9),numbins=numbins,lims=lims, plot=True)
	y_model = model(len(g2), numbins, lims, plot=True)
	print redchisq(bins, y, np.sqrt(y), y_model)
	plt.xlabel('time (ns)')
	plt.ylabel('counts')
	plt.savefig('g2_cw_binsize_{:.0f}ns_range_{:.0f}ns.eps'.format(np.diff(bins)[0],lims[1]), bbox_inches='tight')
	plt.show()

	# plt.figure();plt.plot(bins,y);plt.scatter(bins,y_model);plt.show()