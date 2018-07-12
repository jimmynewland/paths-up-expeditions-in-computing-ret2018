
# coding: utf-8

# # NSF Expeditions in computing Research Experience for Teachers 2018
# In the summer of 2018, I participated in a summer RET at Rice working in the\
# Scalable Health Labs which are part of the Electrical and Computer Engineering
# at Rice University under the direction of Asutosh Sabharwal.

# In[12]:


""" Author: J Newland https://jimmynewland.com/ newton@jayfox.net
    PATHS-UP/Expeditions in Computing Research Experience for Teachers 2018
    
    Python script to detect peaks from a PPG waveform from a CMS 50D+ Pulse Oximeter
    and produce simple statistics comparing the interbeat interval and the heartrate
    for a syncrhonized reading from a CMS 50D+ and the Pulse Sensor Amped.
    
    The given waveform was taken in one sitting with one subject using the same hand.
    Readings were taken every 2ms using serial input. The firmware for the CMS 50D+
    saves the PPG signal, the heartrate, and the time. The firmware for the Pulse Sensor
    Amped save the PPG signal, the heartrate, the time, and the interbeat interval.
    
    The last cell runs some statistcal comparisons between the 2 datasets.
    
    Scalable Health Labs, ECE, Rice Univ.
    Advisors: A Pai, A Maity, A Sabharwal, A Veeraraghavan
    NSF Expeditions in Compting Project Page: http://seebelowtheskin.rice.edu/
"""
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d
plt.style.use('ggplot')
plt.style.use('seaborn-poster')
print(plt.style.available)
from matplotlib import gridspec
#get_ipython().magic(u'matplotlib notebook')
alpha = 0.8


# In[13]:


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs #Nyquist frequeny is half the sampling frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


# In[14]:


def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# In[15]:


def find2nd_deriv(t, ppg):
    y = ppg
    x = t
    
    dy = np.zeros(y.shape,np.float)
    dy[0:-1] = np.diff(y)/np.diff(x)
    dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
    
    d2y = np.zeros(y.shape,np.float)
    d2y[-1] = (dy[-1] - dy[-2])/(x[-1] - x[-2])


# In[16]:


""" Function to plot a waveform comparison between the CMS 50D+ and the
    Pulse Sensor Amped. Both a wide range and a single pulse are displayed.
    The data was taken from one person with the sensors attached to the same
    hand and reading from the same script and saved to one synchronized file.
"""
def plot_waveforms():
    cms_ppg, cms_hr, cms_time, amped_ppg, amped_hr, amped_time, amped_ibi = np.loadtxt('cms_and_amped_ibi.csv', delimiter=',', unpack=True)
    
    amped_ppg = amped_ppg*255.0/(1024.0*2)+100
    cms_filtered = butter_lowpass_filter(cms_ppg,   60, 500.0,1)
    a_filtered   = butter_lowpass_filter(amped_ppg, 60, 500.0,1)
    
    #cms_filtered = find2nd_deriv(cms_time,cms_filtered)
    
    plt.figure(1)
    plt.subplot(211)
    plt.xlabel('time (s)')
    plt.ylabel('PPG Signal')
    plt.title('Photoplethysmogram: CMS 50D+ and Pulse Sensor Amped')
    plt.plot(cms_time,cms_filtered,cms_time,a_filtered)
    plt.xlim(26,32)
    #plt.ylim(ymax=225)
    plt.ylim(ymin=110)
    plt.legend(['CMS 50D+','P.S. Amped'],loc='best', shadow=True)
    plt.tight_layout()
    
    plt.subplot(212)
    plt.xlabel('time (s)')
    plt.ylabel('PPG Signal')
    plt.title('Single Pulse Synchronization')
    plt.plot(cms_time,cms_filtered,amped_time,a_filtered)
    plt.xlim(26,27)
    plt.ylim(ymin=140)
    plt.legend(['CMS 50D+','P.S. Amped'],loc='best', shadow=True)
    
    plt.tight_layout()
    
    plt.show()

    plt.figure(2)
    plt.subplot(211)
    plt.xlabel('time (s)')
    plt.ylabel('PPG Signal')
    plt.title('Photoplethysmogram: CMS 50D+')
    plt.plot(cms_time,cms_filtered)
    plt.xlim(26.21,28.75)
    plt.ylim(ymax=210)
    plt.ylim(ymin=140)
    plt.legend(['CMS 50D+','P.S. Amped'],loc='best', shadow=True)
    plt.tight_layout()
    
    plt.subplot(212)
    plt.xlabel('time (s)')
    plt.ylabel('PPG Signal')
    plt.title('Photoplethysmogram: Pulse Sensor Amped')
    plt.plot(amped_time,a_filtered,color='C1',label='P.S. Amped')
    plt.xlim(26.2,28.9)
    plt.ylim(ymin=130)
    plt.legend(['P.S. Amped','P.S. Amped'],loc='best', shadow=True)
        
    
    plt.tight_layout()
    plt.show()

    plt.figure(3)
    plt.xlabel('time (s)')
    plt.ylabel('PPG Signal')
    plt.title('Example Photoplethysmogram')
    plt.plot(amped_time,a_filtered,color='C1')
    plt.xlim(26.25,27.1)
    plt.ylim(ymin=140)
    plt.show()
    


# In[17]:


""" Function to compare the IBI for the CMS 50D+ and the Pulse
    Sensor Amped. The inputs are arrays for the CMS 50D+ PPG, 
    the time from CMS 50D+, and Pulse Sensor Amped and must be
    the same length.
    The stats of the 2 data sets are compared.
"""
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
        # Inspection shows signal peaks in dataset above 190.
        # The 2nd check confirms we passed a peak.
        # Last check is avoid the dicrotic notch and diastolic peak.
        if cms_ppg[i] > 190 and cms_ppg[i] <= last_ppg and cms_time[i] - last_time > 500: 
            curr_ibi = cms_time[i] - last_time       
            cms_ibi = np.append(cms_ibi,curr_ibi)
            a_ibi = np.append(a_ibi,amped_ibi[i])
            ibi_time = np.append(ibi_time,cms_time[i])
            last_time = cms_time[i]
        last_ppg = cms_ppg[i]

    print(len(ibi_time))

    cms_hist,cms_bins= np.histogram(cms_ibi)
    a_hist,a_bins = np.histogram(a_ibi)

    cms_median_ibi = np.median(cms_ibi)
    a_median_ibi = np.median(a_ibi)

    cms_mean_ibi = np.mean(cms_ibi)
    a_mean_ibi = np.mean(a_ibi)

    cms_std_ibi = np.std(cms_ibi)
    a_std_ibi = np.std(a_ibi)

    hrv_timedomain = dict()
   
    hrv_timedomain['cms_median_ibi'] = cms_median_ibi
    hrv_timedomain['a_median_ibi']   = a_median_ibi

    hrv_timedomain['cms_mean_ibi']   = cms_mean_ibi
    hrv_timedomain['a_mean_ibi']     = a_mean_ibi
    
    hrv_timedomain['cms_std_ibi']    = cms_std_ibi
    hrv_timedomain['a_std_ibi']      = a_std_ibi
     
    stats_results = 'Peak to Peak\nIBI (ms)\tMean\tMed\tStd.\n'
    cms_stats =     'CMS 50D+:\t{:6.2f}\t{:6.2f}\t{:6.2f}\n'
    a_stats =       '   Amped:\t{:6.2f}\t{:6.2f}\t{:6.2f}'
    
    stats_results = stats_results+cms_stats+a_stats
    
    print(stats_results.format(cms_mean_ibi,cms_median_ibi,cms_std_ibi,a_mean_ibi,a_median_ibi,a_std_ibi))

    plt.figure(4)
    plt.subplot(211)
    plt.xlabel('time (ms)')
    plt.ylabel('IBI (ms)')
    plt.title('Interbeat Interval: CMS 50D+ and Pulse Sensor Amped')
    plt.tight_layout()
    plt.plot(ibi_time,cms_ibi,ibi_time,a_ibi)
    plt.legend(['CMS 50D+','P.S. Amped'],loc='best', shadow=True)
        
    plt.subplot(212)
    plt.xlabel('intervals')
    plt.ylabel('frequency')
    plt.title('CMS 50D+ and P.S. Amped IBI Histogram')
    plt.hist(cms_ibi, histtype='stepfilled', alpha=alpha, density=True, bins=5, label='CMS 50D+')
    plt.hist(amped_ibi, histtype='stepfilled', alpha=alpha, density=True, bins=5, label='P.S. Amped')    
    legend = plt.legend(loc='best', shadow=True)

    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')
    plt.tight_layout()

    plt.show()
    
    plt.figure(6)
    plt.subplot(211)
    plt.xlabel('time (ms)')
    plt.ylabel('IBI (ms)')
    plt.title('CMS 50D+ Heart Rate Variability')
    plt.tight_layout()
    plt.plot(ibi_time,cms_ibi, label='CMS 50D+')
    plt.legend(loc='best', shadow=True)
        
    plt.subplot(212)
    plt.hist(cms_hr, histtype='stepfilled', alpha=alpha, density=True, bins=7, label='CMS 50D+')#, rwidth = 0.2)
    plt.xlabel('intervals')
    plt.ylabel('frequency')
    plt.title('CMS 50D+ HRV Histogram')
    legend = plt.legend(loc='best', shadow=True)
    
    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')
    plt.tight_layout()
    plt.show()
    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')
    plt.tight_layout()

    plt.show()
    return hrv_timedomain, cms_ibi, ibi_time


# In[18]:


""" Function to compare the heartrate for the CMS 50D+ and the 
    Pulse Sensor Amped. The inputs are arrays for the CMS 50D+ HR, 
    Pulse Sensor Amped HR, and corresponding read times and must be
    the same length.
    The stats of the 2 data sets are compared.
"""
def hr_stats(cms_hr, amped_hr,times):
    cms_median_hr = np.median(cms_hr)
    a_median_hr = np.median(amped_hr)

    cms_mean_hr = np.mean(cms_hr)
    a_mean_hr = np.mean(amped_hr)

    cms_std_hr = np.std(cms_hr)
    a_std_hr = np.std(amped_hr)

    stats_results = ' HR (BPM)\tMean\tMed\tStd.\n'
    cms_stats =     'CMS 50D+:\t{:5.2f}\t{:5.2f}\t{:5.2f}\n'
    a_stats =       '   Amped:\t{:5.2f}\t{:5.2f}\t{:5.2f}'

    stats_results = stats_results+cms_stats+a_stats

    print(stats_results.format(cms_mean_hr,cms_median_hr,cms_std_hr,a_mean_hr,a_median_hr,a_std_hr))

    #kwargs = dict()

    plt.figure(5)
    plt.subplot(211)
    plt.xlabel('time (ms)')
    plt.ylabel('HR (BPM)')
    plt.title('Heart Rate (BPM): CMS 50D+ and Pulse Sensor Amped')
    plt.tight_layout()
    plt.plot(times,cms_hr,times,amped_hr)
    plt.legend(['CMS 50D+','P.S. Amped'],loc='best', shadow=True)

    plt.subplot(212)
    plt.hist(cms_hr, histtype='stepfilled', alpha=alpha, density=True, bins=5, label='CMS 50D+')#, rwidth = 0.2)
    plt.hist(amped_hr, histtype='stepfilled', alpha=alpha, density=True, bins=5, label='P.S. Amped')#, rwidth = 0.2)
    plt.xlabel('intervals')
    plt.ylabel('frequency')
    plt.title('Heart Rate Histograms')
    legend = plt.legend(loc='best', shadow=True)
    
    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')
    plt.tight_layout()
    plt.show()


# In[19]:


def get_ppg_correlation():
    cms_ppg, cms_hr, cms_time, amped_ppg, amped_hr, amped_time, amped_ibi = np.loadtxt('cms_and_amped_ibi.csv', delimiter=',', unpack=True)
    
    amped_ppg = amped_ppg*255.0/(1024.0*2)
    cms_filtered = butter_lowpass_filter(cms_ppg,   60, 500.0,1)
    a_filtered   = butter_lowpass_filter(amped_ppg, 60, 500.0,1)
    
    x = cms_filtered[100:150]
    y = a_filtered[100:150]
    
    print(len(x))
    print(len(y))
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2)
    ax1.grid(True)
    ax1.axhline(0, color='black', lw=2)

    #ax2 = fig.add_subplot(212, sharex=ax1)
    #ax2.acorr(x, usevlines=True, normed=True, maxlags=50, lw=2)
    #ax2.grid(True)
    #ax2.axhline(0, color='black', lw=2)

    plt.show()
    
    print(np.correlate(x,y))


# In[20]:


# The Numpy loadtxt function unpacks the CSV with columns shown here.
cms_ppg, cms_hr, cms_time, amped_ppg, amped_hr, amped_time, amped_ibi = np.loadtxt('cms_and_amped_ibi.csv', delimiter=',', unpack=True)

# Convert into milliseconds
cms_time = cms_time*1000

# Keep up with the size of the datasets
num_rows = len(cms_ppg)


# In[21]:


plot_waveforms()
hrv_timedomain, cms_ibi, ibi_times = ibi_stats(cms_ppg, cms_time, amped_ibi)
hr_stats(cms_hr, amped_hr, cms_time)
#get_ppg_correlation()

