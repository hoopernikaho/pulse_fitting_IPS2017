"""

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 17})

"""500ns demo: differentiation"""
trace = np.loadtxt('500ns_sig.dat')
dtrace = np.loadtxt('500ns_dsig.dat')

plt.figure()
plt.plot(trace[:,0]*1e9,trace[:,1]*1e3,label='signal')
plt.plot(dtrace[:,0]*1e9,dtrace[:,1]*1e3,label='D(signal)') #savgol filtering over 301*2ns ~ 600ns (2MHz???) , order=3 before differentiating
plt.legend()
plt.ylabel('Voltage (mV')
plt.xlabel('time (ns)')
plt.savefig('edge_detection_by_diff.eps', bbox_inches='tight')