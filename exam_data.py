import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

accel_gyro_data = pd.read_csv("log.txt", '\t')
print(accel_gyro_data.head(10))

ag_data1 = accel_gyro_data[accel_gyro_data['sensor']==1]
ag_data2 = accel_gyro_data[accel_gyro_data['sensor']==2]
ag_data1 = ag_data1.assign(t=pd.Series(np.arange(0, len(ag_data1))).values)
ag_data2 = ag_data2.assign(t=pd.Series(np.arange(0, len(ag_data2))).values)
print(ag_data1.drop('t', axis=1).drop('sensor', axis=1).drop('time', axis=1).describe())
print(ag_data2.drop('t', axis=1).drop('sensor', axis=1).drop('time', axis=1).describe())

ag_data1[['ax','ay','az']].plot()
ag_data2[['ax','ay','az']].plot()
plt.show()

#ag_data1[['az']].plot()
#ag_data1[['az']][500:800].plot()
