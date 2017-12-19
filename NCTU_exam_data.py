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
    plt.show()

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

def plot_xyz(x, y, z, title):
    _time = np.arange(0,len(y))
    plt.figure(figsize=[16,4])
    plt.plot(_time, x, 'r', _time, y, 'g', _time, z, 'b', linewidth=0.5)
    plt.title(title)
    plt.tight_layout()
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--datafile', type=str, default='./Gsensor_data_dbw1.txt', help='the sensor raw data filename')
args = parser.parse_args()
datafile = args.datafile

accel_data = pd.read_csv(datafile, '\t')
print(accel_data.head(10))

# fields : ax	ay	az
accel_data['norm'] = pd.Series(LA.norm(accel_data.as_matrix(), axis=1)) # np.sqrt(np.sum(a1_xyz*a1_xyz, axis=1))

plot_xyz(accel_data['ax'].as_matrix(), accel_data['ay'].as_matrix(), accel_data['az'].as_matrix(),'Accelerometer')
