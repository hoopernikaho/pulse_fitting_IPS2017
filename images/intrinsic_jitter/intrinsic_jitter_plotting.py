"""
Script
	plots amplitude noise projection onto timing axis 
	uses average pulse and error of pulse to search for smallest jitter.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 20})

def find_idx(time_v, t0):
	return np.argmin(np.abs(time_v - t0))

data = np.loadtxt('1ph_model_with_errors_(signal_f).txt')
time_f, signal_f, signal_var_f = data[:,0],data[:,1],data[:,2]
# print time_f, signal_f, signal_var_f 

"""Select only a region where the pulse is one-to-one"""
sig_top = (signal_f+signal_var_f)[(time_f>-1e-7)&(time_f<1e-7)]
sig_bot = (signal_f-signal_var_f)[(time_f>-1e-7)&(time_f<1e-7)]
sig = signal_f[(time_f>-1e-7)&(time_f<1e-7)]
time_less = time_f[(time_f>-1e-7)&(time_f<1e-7)]
print ('mean signal stdev {}'.format(np.mean(signal_var_f)))

jitter = lambda h: time_less[find_idx(sig_bot,h)]-time_less[find_idx(sig_top,h)]

"""Plots jitter as a function of signal height"""
# plt.figure();plt.plot(sig,map(jitter,sig))
jitters = map(jitter,sig)
min_jitter_at = sig[np.argmin(jitters)]
print ('Minimum jitter is {}ns at height {}'.format(np.min(jitters)*1e9, min_jitter_at))

"""Plots intrinsic jitter concept diagram"""
plt.figure()
plt.fill_between(time_f*1e9,
	signal_f+signal_var_f,
	signal_f-signal_var_f,
	color='grey')
plt.plot(time_f*1e9, signal_f, linewidth = 2, color='black')
xmin=-500
xmax=1500
ymin=-0.005
ymax=0.02
plt.ylim(ymin,ymax)
plt.xlim(xmin,xmax)
plt.xlabel('time (ns)')
plt.ylabel('voltage (V)')

plt.hlines(min_jitter_at, xmin, xmax, linestyle='--')
plt.vlines(time_less[find_idx(sig_top,min_jitter_at)]*1e9, ymin, min_jitter_at, linestyle='--')
plt.vlines(time_less[find_idx(sig_bot,min_jitter_at)]*1e9, ymin, min_jitter_at, linestyle='--')

plt.annotate('',
	(time_less[find_idx(sig_top,min_jitter_at)]*1e9, -2e-3),
	(time_less[find_idx(sig_bot,min_jitter_at)]*1e9, -2e-3),
	arrowprops={'arrowstyle':'<|-|>'})

# plt.text(0,-2e-3, r'2$\Delta t_{\sigma}\approx 22$ ns ', va = 'bottom', ha = 'left') #22 ns from ./intrinsic_jitter_histogram/
plt.text(0,-2e-3, r'FWHM$\approx 22$ ns ', va = 'bottom', ha = 'left') #22 ns from ./intrinsic_jitter_histogram/

plt.savefig('jitter.eps', bbox_inches='tight')
# plt.show()