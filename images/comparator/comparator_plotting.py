import matplotlib
matplotlib.rcParams.update({'font.size': 20})
import matplotlib.pyplot as plt
import numpy as np
# import sys
# sys.path.insert('/workspace/projects/TES/scripts/')
# import pulse_discrimination as pf

trace = np.loadtxt('sample_500ns_sep_trace')
comparator = np.loadtxt('sample_500ns_sep_trace_comparator')

time, signal = trace[:,0]*1e9, trace[:,1]*1e3
_, mask = comparator[:,0], comparator[:,1]
height_th = 0.0075
plt.figure()
plt.xlim(-2000,7500)
plt.plot(time,signal)
plt.plot(time,mask*np.max(signal),label='logic')
plt.xlabel('time (ns)')
plt.ylabel('Voltage (mV)')
plt.legend()
plt.savefig('comparator_at_500ns.eps')

plt.figure()
plt.xlim(-2000,7500)
plt.plot(time,signal)
plt.xlabel('time (ns)')
plt.ylabel('Voltage (mV)')
plt.hlines(5, -4000, 8000, linestyle='--')
plt.text(-1000, 5, 'threshold')
plt.savefig('overlapping_pulses.eps')
plt.show()