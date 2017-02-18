"""
This script outlines the functions to run in order to obtain the g2 of overlapping TES pulses, that have an expected separation given by the pulse-pair separation of an 810~nm diode.

Procedure to fit pulses:
0. Filter to get n=2 pulses
1. Identify height at time that corresponds to two single-photon pulses overlapping.
	i.e. reject n=2+n=0 events.
	Filter for these pulses.
2. Fit, plot g2
"""

directory_name_1us = '/workspace/projects/TES/data/20170126_TES5_n012_distinguishibility_20MHz_tau_vs_offset/1us/'
filelist_source_1us = np.array(glob.glob(directory_name_1us + '*.trc'))

""" sample areas to plot a sample """

data_source_1us = np.array([param_extr(f, t_initial=None, t_final=None, h_th=height_th)
                 for f
                 in tqdm.tqdm(filelist_source_1us[:20000])])

areas_source_1us = data_source_1us['area_win']

mask_2ph_source_1us = (areas_source_1us > 0.9)&(areas_source_1us < 1.556)

plt.figure();pplot(filelist_source_1us[:20000][mask_2ph_source_1us][:5000],density=10,plot_every=10)

#identify region that identifies pulse pairs, for t0

data_source_1us = np.array([param_extr(f, t_initial=None, t_final=None, h_th=height_th,t0=.5e-6)
                 for f
                 in tqdm.tqdm(filelist_source_1us[:20000][mask_2ph_source_1us])])

plt.figure();plt.hist(data_source_1us['heightattime'],400);plt.show()

heightattimes = data_source_1us['heightattime']

mask_1us = (heightattimes>.00406)&(heightattimes<.0197)

plt.figure();pplot(filelist_source_1us[:20000][mask_2ph_source_1us][mask_1us])

results_1us= np.array([fit_two(*trace_extr(file))
						for file
						in tqdm.tqdm(filelist_source_1us[:20000][mask_2ph_source_1us][mask_1us])])

processed_1us = extract(results_1us[:,0])

plt.figure();plt.hist(np.abs(processed_1us._tau)*1e9,400,range=([700,1400]));plt.show()

np.savetxt(results_directory+'1us_separation_tau.txt',processed_1us._tau)
