import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import glob
import sys
sys.path.insert(0,'/workspace/projects/TES/scripts/')
import lecroy


def trc2dat(filelist, out_folder=None):
    """batch conversion of lecroy binary traces to ASCII files"""
    for f in filelist:
        trc = lecroy.LecroyBinaryWaveform(f)
        time = trc.mat[:, 0]
        signal = trc.mat[:, 1]
        fname = f.strip('.trc').split('/')[-1]
        fname = out_folder + fname + '.dat'
        with open(fname, 'w') as f:
            f.write('#time\tvoltage\n')
            [f.write('{}\t{}\n'.format(t, v))
             for t, v
             in zip(time, signal)]


def save_sample_traces(filelist, sample_trace_directory_name=None):
    """
    Generates traces in the sample_pulse folder
    :param filelist: list of lecroy traces in the raw data directory
        specified in the README file.
    """

    for f in filelist:
        trc = lecroy.LecroyBinaryWaveform(f)
        time = trc.mat[:, 0]
        signal = trc.mat[:, 1]
        fname = f.strip('.trc').split('/')[-1]
        np.savetxt(sample_trace_directory_name + fname +
                   '.txt', np.array(zip(time, signal)))


def load_sample_traces(sample_trace_directory_name):
    sample_traces = []
    for f in glob.glob(sample_trace_directory_name + '*.dat'):
        trc = np.loadtxt(f)
        time = trc[:, 0]
        signal = trc[:, 1]
        # print time,signal
        sample_traces.append(np.array(zip(time, signal)))
    return np.array(sample_traces)


def pplot(sample_trace_directory_name, plot_every=1):
    """generates a lightweight plot of some sample traces
    WARNING: does not automatically remove trace dc offset
    :params density: plot every 'density' number of traces
    """
    plt.figure('persistence plot')
    sample_traces = load_sample_traces(sample_trace_directory_name)
    # print sample_traces
    for trc in sample_traces:
        time = trc[:, 0]
        signal = trc[:, 1]
        plt.plot(time[::plot_every] * 1e9, signal[::plot_every]*1e3, alpha=0.3)
    plt.xlabel('time (ns)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(0, 3000)
    plt.savefig('persistence.pdf')
    # plt.show()
matplotlib.rcParams.update({'font.size': 20})
pplot('./sample_traces/', 10)
