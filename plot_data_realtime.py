import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from drawnow import drawnow, figure
import os
import argparse
import serial
import math
from pynput import mouse

def make_fig():
    global plot_switch
    y1_max, y1_min = max(accel1_norm_y), min(accel1_norm_y)
    y2_max, y2_min = max(accel2_norm_y), min(accel2_norm_y)
    plt.ylim(ymax=max(y1_max, y2_max)+500, ymin=min(y1_min, y2_min)-500)
    if plot_switch == 1:
        plt.plot(time_x, accel1_norm_y, 'g', linewidth=0.5)
    elif plot_switch == 2:
        plt.plot(time_x, accel2_norm_y, 'r', linewidth=0.5)
    else:
        plt.plot(time_x, accel1_norm_y, 'g', time_x, accel2_norm_y, 'r', linewidth=0.5)
    plt.text(time_x[-1], y1_max+100, '%.2f / %.2f' % (y1line_max[0], y1line_min[0]), color='green', ha='right', va='bottom')
    plt.text(time_x[-1], y2_min-150, '%.2f / %.2f' % (y2line_max[0], y2line_min[0]), color='red', ha='right', va='bottom')
    '''
    y1_max, y1_min = y1line_max[0], y1line_min[0]
    y2_max, y2_min = y2line_max[0], y2line_min[0]
    plt.ylim(ymax=max(y1_max, y2_max)+1000, ymin=min(y1_min, y2_min)-1000)
    plt.plot(time_x, accel1_norm_y, 'g',
             time_x, accel2_norm_y, 'r',
             time_x, y1line_max[:len(time_x)], 'g--',
             time_x, y1line_min[:len(time_x)], 'g--',
             time_x, y2line_max[:len(time_x)], 'r--',
             time_x, y2line_min[:len(time_x)], 'r--', linewidth=0.5) # b,g,r,c,m,y,k,w
    plt.text(time_x[-1], y1_max, '%.2f' % y1_max, color='green', ha='right', va='bottom')
    plt.text(time_x[-1], y1_min-10, '%.2f' % y1_min, color='green', ha='right', va='top')
    plt.text(time_x[-1], y2_max, '%.2f' % y2_max, color='red', ha='right', va='bottom')
    plt.text(time_x[-1], y2_min-10, '%.2f' % y2_min, color='red', ha='right', va='top')
    '''

def on_click(x, y, button, pressed):
    global plot_switch
    global is_plotting

    if not pressed:
        is_plotting = not is_plotting
        if is_plotting == 1:
            plot_switch += 1
            if plot_switch == 3:
                plot_switch = 0
    
    '''
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False
    '''

TIME_X_RANGE = 500

accel1_xyz_list = []
accel2_xyz_list = []
accel1_norm_y = []
accel2_norm_y = []
time_x = []

y1line_max = [0.0] * TIME_X_RANGE
y1line_min = [65535.0] * TIME_X_RANGE
y2line_max = [0.0] * TIME_X_RANGE
y2line_min = [65535.0] * TIME_X_RANGE

listener = mouse.Listener(on_click=on_click)
listener.start()

#with open('log_30sec_1.txt', 'r') as ser:
with serial.Serial('/dev/ttyUSB0', 115200, timeout=10) as ser:
    global plot_switch
    global is_plotting

    plot_switch = 0 # 0: plot both, 1: plot accel1, 2: plot accel2
    is_plotting = 1

    time_idx = 0
    draw_update_cnt = 0
    # fields : [accel] time	ax1	ay1	az1 ax2 ay2 az2
    for _byte_line in ser: # data_line = ser.readline() # ser.readlines()
        if is_plotting == 0:
            continue

        data_line = _byte_line.decode('utf-8')
        if not data_line.startswith('[accel]'):
            print('[Data ValueError]: ' + data_line)
            continue

        field_data = data_line.split('\t')
        accel1_xyz = np.array([int(field_data[2]), int(field_data[3]), int(field_data[4])])
        accel2_xyz = np.array([int(field_data[5]), int(field_data[6]), int(field_data[7])])
        #accel1_xzy_list.append(accel1_xyz)
        #accel2_xzy_list.append(accel2_xyz)
        l2_norm1 = math.sqrt(accel1_xyz.dot(accel1_xyz)) # sqrt(x**2+y**2+z**2)
        l2_norm2 = math.sqrt(accel2_xyz.dot(accel2_xyz))

        if y1line_max[0] < l2_norm1:
            y1line_max[:] = [l2_norm1 for _y in y1line_max]
        if y1line_min[0] > l2_norm1:
            y1line_min[:] = [l2_norm1 for _y in y1line_min]
        if y2line_max[0] < l2_norm2:
            y2line_max[:] = [l2_norm2 for _y in y2line_max]
        if y2line_min[0] > l2_norm2:
            y2line_min[:] = [l2_norm2 for _y in y2line_min]

        time_idx += 1
        time_x.append(time_idx)
        accel1_norm_y.append(l2_norm1)
        accel2_norm_y.append(l2_norm2)
        draw_update_cnt += 1
        if draw_update_cnt == 30:
            drawnow(make_fig)
            draw_update_cnt = 0
        if len(time_x) == TIME_X_RANGE:
            time_x.pop(0)
            accel1_norm_y.pop(0)
            accel2_norm_y.pop(0)
    #plt.show()

print(len(accel1_xyz_list))
print(len(accel2_xyz_list))
