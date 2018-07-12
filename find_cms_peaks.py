import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
plt.style.use('seaborn-white')

def ibi_stats(cms_ppg, cms_time, amped_ibi):
    cms_ibi = []
    cms_ibi = np.array(cms_ibi)

    a_ibi = []
    a_ibi = np.array(a_ibi)

    ibi_time = []
    ibi_time = np.array(ibi_time)

    last_ppg = 0
    last_time = cms_time[0]

    #find peaks in CMS PPG
    for i in range(1,num_rows):
        if cms_ppg[i] > 190 and cms_ppg[i] <= last_ppg and cms_time[i] - last_time > 500: 
            curr_ibi = cms_time[i] - last_time       
            cms_ibi = np.append(cms_ibi,curr_ibi)
            a_ibi = np.append(a_ibi,amped_ibi[i])
            ibi_time = np.append(ibi_time,cms_time[i])
            last_time = cms_time[i]
        last_ppg = cms_ppg[i]

    cms_hist,cms_bins= np.histogram(cms_ibi)
    a_hist,a_bins = np.histogram(a_ibi)

    cms_median_ibi = np.median(cms_ibi)
    a_median_ibi = np.median(a_ibi)

    cms_avg_ibi = np.average(cms_ibi)
    a_avg_ibi = np.average(a_ibi)

    cms_std_ibi = np.std(cms_ibi)
    a_std_ibi = np.std(a_ibi)

    stats_results = '         \tAvg\tMed\tStd.\n'
    cms_stats =     'CMS D50+:\t{:6.2f}\t{:6.2f}\t{:6.2f}\n'
    a_stats =       '   Amped:\t{:6.2f}\t{:6.2f}\t{:6.2f}'

    stats_results = stats_results+cms_stats+a_stats

    print(stats_results.format(cms_avg_ibi,cms_median_ibi,cms_std_ibi,a_avg_ibi,a_median_ibi,a_std_ibi))

    kwargs = dict(histtype='stepfilled', alpha=0.9, normed=True, bins=20)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(ibi_time,cms_ibi,ibi_time,a_ibi)
    plt.subplot(312)
    plt.hist(cms_ibi, **kwargs)
    plt.subplot(313)
    plt.hist(a_ibi, **kwargs)

    plt.show()

def hr_stats(cms_hr, amped_hr,times):
    cms_median_hr = np.median(cms_hr)
    a_median_hr = np.median(amped_hr)

    cms_avg_hr = np.average(cms_hr)
    a_avg_hr = np.average(amped_hr)

    cms_std_hr = np.std(cms_hr)
    a_std_hr = np.std(amped_hr)

    stats_results = '         \tAvg\tMed\tStd.\n'
    cms_stats =     'CMS D50+:\t{:6.2f}\t{:6.2f}\t{:6.2f}\n'
    a_stats =       '   Amped:\t{:6.2f}\t{:6.2f}\t{:6.2f}'

    stats_results = stats_results+cms_stats+a_stats

    print(stats_results.format(cms_avg_hr,cms_median_hr,cms_std_hr,a_avg_hr,a_median_hr,a_std_hr))

    kwargs = dict(histtype='stepfilled', alpha=0.9, normed=True, bins=20)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(times,cms_hr,times,amped_hr)
    plt.subplot(312)
    plt.hist(cms_hr, **kwargs)
    plt.subplot(313)
    plt.hist(amped_hr, **kwargs)

    plt.show()

cms_ppg, cms_hr, cms_time, amped_ppg, amped_hr, amped_time, amped_ibi = np.loadtxt('cms_and_amped_ibi.csv', delimiter=',', unpack=True)

cms_time = cms_time*1000
num_rows = len(cms_ppg)

ibi_stats(cms_ppg, cms_time, amped_ibi)
hr_stats(cms_hr, amped_hr,cms_time)