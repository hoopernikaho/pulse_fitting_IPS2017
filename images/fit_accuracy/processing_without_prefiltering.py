"""
This script outlines the functions to run in order to obtain the g2 of overlapping TES pulses, 
that have an expected separation given by the pulse-pair separation of an 810~nm diode.

Procedure to fit pulses:
0. Filter to get n=2 pulses
1. Identify height at time that corresponds to two single-photon pulses overlapping.
	i.e. reject n=2+n=0 events.
	Filter for these pulses.
2. Fit, plot g2
"""
height_th = 0.0075
signal_fs = signal_f
time_f, signal_fs = time_f[:-100], signal_fs[:-100]

directory_name_200ns = '/workspace/projects/TES/data/20170126_TES5_n012_distinguishibility_20MHz_tau_vs_offset/200ns/'
filelist_source_200ns = np.array(glob.glob(directory_name_200ns + '*.trc'))

""" sample areas to plot a sample """

data_source_200ns = np.array([param_extr(f, t_initial=None, t_final=None, h_th=height_th)
                 for f
                 in tqdm.tqdm(filelist_source_200ns[:200])])

areas_source_200ns = data_source_200ns['area_win']

mask_2ph_source_200ns = (areas_source_200ns > 0.9)&(areas_source_200ns < 1.57)
plt.figure();pplot(filelist_source_200ns[:200][mask_2ph_source_200ns],density=10,plot_every=10)

plt.figure();pplot(filelist_source_200ns[:20000][mask_2ph_source_200ns][:5000],density=10,plot_every=10)


#identify region that identifies pulse pairs, for t0

# data_source_200ns = np.array([param_extr(f, t_initial=None, t_final=None, h_th=height_th,t0=.5e-6)
#                  for f
#                  in tqdm.tqdm(filelist_source_200ns[:20000][mask_2ph_source_200ns])])

# plt.figure();plt.hist(data_source_200ns['heightattime'],400);plt.show()

# heightattimes = data_source_200ns['heightattime']

# mask_200ns = (heightattimes>.00406)&(heightattimes<.0197)

# plt.figure();pplot(filelist_source_200ns[:20000][mask_2ph_source_200ns][mask_200ns])

results_200ns= np.array([fit_two(*trace_extr(file))
						for file
						in tqdm.tqdm(filelist_source_200ns[:20000][mask_2ph_source_200ns])])

processed_200ns_ = extract(results_200ns[:,0])

hist(processed_200ns_._tau*1e9,lims=[-700,700]) 

numedges_200ns = [len(i) for i in results_200ns[:,1]]
tau_init_200ns = np.abs(processed_200ns._one_x_offsets_init-processed_200ns._two_x_offsets_init) # time difference between initial offsets

hist(tau_init_200ns*1e9,lims=[-700,700]) 
plt.plot(tau_init_200ns*1e9, numedges, '.')

processed_200ns_less = offset_amplitude_data_200ns = np.array(
	zip(processed_200ns._one_x_offsets,
	processed_200ns._two_x_offsets,
	processed_200ns._one_amplitudes,
	processed_200ns._two_amplitudes),
	dtype=[('one_x_offsets','float64'),
	('two_x_offsets','float64'),
	('one_amplitudes','float64'),
	('two_amplitudes','float64')]
	)


np.savetxt(results_directory+'200ns_separation_offset_amplitude_data.txt',
	processed_200ns_less, 
	header = '\t'.join(processed_200ns_less.dtype.names))


processed_200ns_init = offset_amplitude_data_200ns = np.array(
	zip(processed_200ns._one_x_offsets_init,
	processed_200ns._two_x_offsets_init,
	processed_200ns._one_amplitudes_init,
	processed_200ns._two_amplitudes_init),
	dtype=[('one_x_offsets_init','float64'),
	('two_x_offsets_init','float64'),
	('one_amplitudes_init','float64'),
	('two_amplitudes_init','float64')]
	)

np.savetxt(results_directory+'200ns_separation_offset_amplitude_init_data.txt',
	processed_200ns_init, 
	header = '\t'.join(processed_200ns_init.dtype.names))
# plt.figure();plt.hist(np.abs(processed_200ns._tau)*1e9,400,range=([700,1400]));plt.show()

# np.savetxt(results_directory+'200ns_separation_tau.txt',processed_200ns._tau)

""""""
plt.ion()
for i in np.arange(10):
	plt.figure()
	fit_result = fit_two(
		*trace_extr(filelist_source_200ns[mask_2ph_source_200ns][i])
		)
	fit_result[0].plot_fit()