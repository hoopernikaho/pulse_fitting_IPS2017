"""
The g2 of TES outputs of overlapping pulses is generated and fitted, for various time intervals.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 20})
from lmfit import Parameters
from lmfit.models import GaussianModel
import glob

def fit_gaussian(x,y,debug=False):
	mod = GaussianModel()
	pars = mod.guess(y, x=x)
	out  = mod.fit(y, pars, x=x, weights=(1/(np.sqrt(y))))
	print(out.fit_report())
	if debug:
		plt.figure();out.plot_fit();plt.show()
	# return out.params['center'].value,out.params['center'].stderr
	return out.params['center'].value,out.params['sigma'].value

centers = []
sigmas = []

for f in glob.glob('*.txt'):
	tau = np.loadtxt(f)
	"""estimate center of histogram"""
	g2_init = np.histogram(np.abs(tau)*1e9,400)
	freqi, binsi = g2_init[0],g2_init[1]
	centeri = binsi[np.argmax(freqi)]
	"""fit to gaussian distribution""" 
	g2 = np.histogram(np.abs(tau)*1e9,100,range=([centeri-300,centeri+300]))
	freq, bins = g2[0], g2[1]
	step = np.diff(bins)[0]
	bins = bins[:-1] + step / 2.
	center, sigma = fit_gaussian(bins[freq>0], freq[freq>0], debug=True)
	centers.append(center)
	sigmas.append(sigma)

"""
diode data: 
/workspace/projects/TES/data/20170126_TES5_n012_distinguishibility_20MHz_tau_vs_offset/diode pulses/
"""
# diode_separation = [188.4,481.6,652.4,938.8]
# diode_widths = [3.6+2.8,4+4,3.6+2.8,4+2.8]
diode_separation = [481.6,652.4,938.8]
diode_widths = [4+4,3.6+2.8,4+2.8]

centers=np.array(centers)
sigmas=np.array(sigmas)
plt.figure()
plt.errorbar(diode_separation,np.sort(centers),xerr=diode_widths,yerr=sigmas[np.argsort(centers)],ls='none')
plt.plot(diode_separation,diode_separation)
plt.xlabel('diode pulse separation (ns)')
plt.ylabel('TES pulse separation (ns)')
# plt.title('Fitted Pulse separation vs Diode Pulse separation')
plt.savefig('fitted_vs_actual_pulse_separation.eps', bbox_inches='tight')

plt.figure()
plt.errorbar(diode_separation,np.sort(centers)-diode_separation,xerr=diode_widths,yerr=sigmas[np.argsort(centers)]+diode_widths,ls='none')
plt.show()