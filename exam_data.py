import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse
import librosa
import librosa.display
import math
from numpy import linalg as LA

def plot_power_spectrom(liner_freq_spectrom, title):
    plt.figure(figsize=[16,4])
    librosa.display.specshow(librosa.amplitude_to_db(liner_freq_spectrom, ref=np.max), sr=100, hop_length=32, x_axis='time', y_axis='log');
    plt.title(title)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    #plt.show()

def estimated_autocorrelation(x):
    """
    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    assert np.allclose(r, np.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result

def plot_xy(y, title):
    x = np.arange(0,len(y))
    plt.figure(figsize=[16,4])
    plt.plot(x, y, 'r', linewidth=0.5)
    plt.title(title)
    plt.tight_layout()
    #plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--datafile', type=str, default='./log_teacupmoving.txt', help='the sensor raw data filename')
args = parser.parse_args()
datafile = args.datafile

accels_data = pd.read_csv(datafile, '\t')
#print(accels_data.head(10))

# fields : [accel] time	ax1	ay1	az1 ax2 ay2 az2
accel1_data = accels_data.iloc[:,2:5]
accel2_data = accels_data.iloc[:,5:8]
accel1_data.rename(columns={'ax1':'ax', 'ay1':'ay','az1':'az' }, inplace=True)
accel2_data.rename(columns={'ax2':'ax', 'ay2':'ay','az2':'az' }, inplace=True)

a1_xyz = accel1_data.as_matrix()
a2_xyz = accel2_data.as_matrix()
accel1_data['norm'] = pd.Series(LA.norm(a1_xyz, axis=1)) # np.sqrt(np.sum(a1_xyz*a1_xyz, axis=1))
accel2_data['norm'] = pd.Series(LA.norm(a2_xyz, axis=1)) # np.sqrt(np.sum(a2_xyz*a2_xyz, axis=1))
'''
plot_xy(accel1_data['norm'].as_matrix(), 'Accel1 Signal')
plot_xy(accel2_data['norm'].as_matrix(), 'Accel2 Signal')
'''
'''
#accel3_data = accel1_data.subtract(accel2_data)
print(accel1_data.describe())
print(accel2_data.describe())
#print(accel3_data.describe())
'''
'''
sgl_amp = accel1_data['norm'].std() * 1.0
print(accel1_data['norm'].mean())
print(accel1_data['norm'].std())
sgl_freq = 5 # 5Hz
t_range = np.arange(len(accel1_data['norm'].as_matrix()))
sgl = np.array([sgl_amp*0.6*np.sin(2*np.pi*sgl_freq*i/100) for i in t_range]) # 100 is accelerometer data output rate
accel1_data['signal'] = pd.Series(sgl)
accel1_data['combine'] = accel1_data['norm'] + accel1_data['signal']
plot_xy(accel1_data['norm'].as_matrix(), 'Accel1 White noise')
plot_xy(accel1_data['signal'].as_matrix(), 'Accel1 Signal')
plot_xy(accel1_data['combine'].as_matrix(), 'Accel1 Combine')
plt.show()
'''
accel1_autocorr = estimated_autocorrelation(accel1_data['norm'].as_matrix())
accel2_autocorr = estimated_autocorrelation(accel2_data['norm'].as_matrix())
plot_xy(accel1_autocorr, 'Accel1 Autocorrelation')
plot_xy(accel2_autocorr, 'Accel2 Autocorrelation')
plt.show()

a1_freq_spectrom = librosa.stft(y=accel1_data['norm'].as_matrix(), n_fft=1024, hop_length=32, window='hamming')
a2_freq_spectrom = librosa.stft(y=accel2_data['norm'].as_matrix(), n_fft=1024, hop_length=32, window='hamming')
plot_power_spectrom(a1_freq_spectrom, 'Accel1 Power Spectrogram')
plot_power_spectrom(a2_freq_spectrom, 'Accel2 Power Spectrogram')
plt.show()

#a1_freq_spectrom_abs = np.abs(a1_freq_spectrom)
a1_freq_spectrom_db = librosa.amplitude_to_db(a1_freq_spectrom, ref=np.max)
a2_freq_spectrom_db = librosa.amplitude_to_db(a2_freq_spectrom, ref=np.max)
plot_xy(a1_freq_spectrom_db[:,50], 'Accel1 Power Spectrogram')
plot_xy(a2_freq_spectrom_db[:,50], 'Accel2 Power Spectrogram')
plt.show()
