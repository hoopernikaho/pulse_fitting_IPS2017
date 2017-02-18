#!/usr/bin/env python2

"""
find the optimal threshold between peaks distributions
"""
import glob
import numpy as np
import peakutils
import matplotlib.pyplot as plt

from scipy.stats import norm

from lmfit import Parameters
from lmfit.models import GaussianModel

def peaks(pnr, min_peak_sep=1, threshold=None):
    """
    Only the peaks with amplitude higher than the threshold will be detected.
    The peak with the highest amplitude is preferred to satisfy minimum
    distance constraint (in units of indices).

    :param pnr: 2D histogram, output of np.histogram()
    :param min_peak_sep: Minimum distance between each detected peak.
    :param threshold: Normalized threshold, float between [0., 1.]
    """
    # unpack the histogram into x and y values
    frequencies = pnr[0]

    # match the number of bins to the frequencies, find the step size
    x_val = pnr[1]
    step = np.diff(x_val)[0]
    x_val = x_val[:-1] + step / 2.

    # heuristic value for the threshold. Input one if you can do better!
    if threshold is None:
        threshold = np.median(frequencies) / np.max(frequencies) + .05

    # the dirty work
    indexes = peakutils.indexes(frequencies,
                                thres=threshold,
                                min_dist=int(min_peak_sep / step))
    indexes.sort()
    return x_val[indexes], frequencies[indexes]


def gauss_fit_interp(pnr, min_peak_sep, threshold=None, weighted=False):
    """
    improve the precision in the location of the peaks by fitting them
    using a sum of Gaussian distributions
    :param pnr: 2D histogram, output of np.histogram
    :param min_peak_sep: Minimum distance between each detected peak.
    :param threshold: Normalized threshold, float between [0., 1.]
    :param weighted: if True, it associate a poissonian error to the
        frequencies
    """

    # unpack the histogram into x and y values
    frequencies = pnr[0]

    # match the number of bins to the frequencies, find the step size
    x_val = pnr[1]
    step = np.diff(x_val)[0]
    x_val = x_val[:-1] + step / 2.

    # find a first approximation of the peak location using local differences
    peaks_pos, peak_height = peaks(pnr, min_peak_sep, threshold)

    # build a fitting model with a number of gaussian distributions matching
    # the number of peaks
    fit_model = np.sum([GaussianModel(prefix='g{}_'.format(k))
                        for k, _
                        in enumerate(peaks_pos)])

    # Generate the initial conditions for the fit
    p = Parameters()

    p.add('A', np.max(peak_height) * min_peak_sep)
    p.add('n_bar', 3.0)
    # p.add('Delta_E', peaks_pos[-1] - peaks_pos[-2])
    p.add('g0_sigma', min_peak_sep / 5, min=0)
    p.add('sigma_p', min_peak_sep / np.sqrt(2) / np.pi, min=0)

    # Centers
    p.add('g0_center', peaks_pos[0], min=0)
    p.add('g1_center', peaks_pos[1], min=0)
    [p.add('g{}_center'.format(k + 2),
           j,
           # expr='g{}_center + Delta_E'.format(k + 1)
           )
     for k, j
     in enumerate(peaks_pos[2:])]

    # amplitudes
    [p.add('g{}_amplitude'.format(k),
           j * min_peak_sep / np.sqrt(2),
           expr='A * exp(-n_bar) * n_bar**{} / factorial({})'.format(k, k),
           min=0)
     for k, j
     in enumerate(peak_height)]

    # fixed width
    [p.add('g{}_sigma'.format(k + 1),
           min_peak_sep / np.sqrt(2) / np.pi,
           min=0,
           # expr='sigma_p * sqrt({})'.format(k + 1)
           expr='sigma_p'
           )
     for k, _
     in enumerate(peak_height[1:])]

    if weighted:
        # generates the poissonian errors, correcting for zero values
        err = np.sqrt(frequencies)
        err[frequencies == 0] = 1

        result = fit_model.fit(frequencies,
                               x=x_val,
                               params=p,
                               weights=1 / err,
                               # method='nelder'
                               )
    else:
        result = fit_model.fit(frequencies, x=x_val, params=p)

    # amplitudes = np.array([result.best_values['g{}_amplitude'.format(k)]
    #                        for k, _
    #                        in enumerate(peaks_pos)])
    # centers = np.array([result.best_values['g{}_center'.format(k)]
    #                     for k, _
    #                     in enumerate(peaks_pos)])
    # sigmas = np.array([result.best_values['g{}_sigma'.format(k)]
    #                    for k, _
    #                    in enumerate(peaks_pos)])
    # s_vec = centers.argsort()
    # plt.plot(x_val, result.best_fit, linewidth=5)
    plt.plot(x_val, result.eval_components()['g0_'], label='n=1',linewidth=5, linestyle='--', color='black')
    plt.plot(x_val, result.eval_components()['g1_'], label='n=2',linewidth=5, linestyle='--', color='red')
    return result


def thresholds(pnr, min_peak_sep, threshold=None, weighted=False):
    """
    halfway point between peaks
    :param pnr: 2d list of histogram
    """
    result = gauss_fit_interp(pnr, min_peak_sep, threshold, weighted)
    centers = np.array([result.best_values['g{}_center'.format(k)]
                        for k, _
                        in enumerate(result.components)])
    s_vec = centers.argsort()
    peaks_pos = centers[s_vec]

    return np.diff(peaks_pos) / 2 + peaks_pos[:-1]


def min_overlap(x0, x1, sigma0, sigma1, samples=1000):
    """
    return threshold value that minimizes the overlap between the given
    gaussian distributions
    """
    x_vec = np.linspace(x0, x1, samples)
    noise = 1 - norm.cdf(x_vec, loc=x0, scale=sigma0)
    sgn = norm.cdf(x_vec, loc=x1, scale=sigma1)
    snr = sgn + noise
    sgn[np.argmin(snr)]
    noise[np.argmin(snr)]
    return x_vec[np.argmin(snr)]

def thresholds_N(pnr, min_peak_sep, threshold=None, weighted=False):
    """
    thresholds between peaks assuming gaussian distributions
    """
    result = gauss_fit_interp(pnr, min_peak_sep, threshold, weighted)

    centers = np.array([result.best_values['g{}_center'.format(k)]
                        for k, _
                        in enumerate(result.components)])
    sigmas = np.array([result.best_values['g{}_sigma'.format(k)]
                       for k, _
                       in enumerate(result.components)])
    s_vec = centers.argsort()

    xs = centers[s_vec]
    ss = sigmas[s_vec]
    N = len(xs)
    return [min_overlap(xs[j], xs[j + 1], ss[j], ss[j + 1])
            for j
            in range(N - 1)]

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    data_folder = '../data/'
    single_pulse_folder = '20161011_g2_signal_unheralded_singlesrate_5.6k/'
    bg = 2000

    trc_single = traces(data_folder + single_pulse_folder, bg)
    pnr = np.histogram(trc_single[2], 200)
    result = gauss_fit_interp(pnr, .7e-8, weighted=True)
    th = thresholds_N(pnr, .7e-8, weighted=True)
    print(result.fit_report())
    print(th)
    result.plot()
    plt.show()


def min_overlap_stats(x0, x1, sigma0, sigma1, samples=1000):
    """
    return threshold value that minimizes the overlap between the given
    gaussian distributions
    """
    x_vec = np.linspace(x0, x1, samples)
    noise = 1 - norm.cdf(x_vec, loc=x0, scale=sigma0)
    sgn = norm.cdf(x_vec, loc=x1, scale=sigma1)
    snr = sgn + noise
    return x_vec[np.argmin(snr)], sgn[np.argmin(snr)], noise[np.argmin(snr)]

# min_overlaps=[min_overlap(aresult.values['g{}_center'.format(k)],aresult.values['g{}_center'.format(k+1)],aresult.values['g{}_sigma'.format(k)],aresult.values['g{}_sigma'.format(k+1)])
# for k in np.arange(7)]