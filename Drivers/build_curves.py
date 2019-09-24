# -- coding: utf-8 --
from __future__ import unicode_literals
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import time


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


def _handler_gen_list(number):
    l = list()
    for i in range(number):
        l.append(i)
    return l


def _handler_for_step(data_len):
    # print('_handler_for_step    {}'.format(data_len))
    return int(data_len / 20) + 1


def _handler_xticks(Value, datetime_mode):
    step = _handler_for_step(len(Value))
    # print(datetime_mode)

    if datetime_mode == 'time':
        xLabel = 'Time'
        xValue = list()
        # print(Value)
        for number, time in enumerate(Value):
            if number % step == 0:
                xValue.append(str(time).split(' ')[1])
            else:
                xValue.append(str())
    else:
        xLabel = 'DateTime'
        xValue = list()
        for number, datetime in enumerate(Value):
            if number % step == 0:
                xValue.append(datetime)
            else:
                xValue.append(str())

    return xValue, xLabel, _handler_gen_list(len(xValue))


def one_plot(Value, yLabel=None, datetime_mode='time', sensor_name='Unknown', grid_mode=False, type_plot='line',
             color='cornflowerblue', linestyle='-', linewidth=2, save_fig=True):
    print(1)
    xValue, xLabel, pattern_for_mask = _handler_xticks(Value[1], datetime_mode)
    yValue = Value[0]
    print(2)
    fig, axs = plt.subplots()
    print(3)
    if type_plot == 'line':
        axs.plot(pattern_for_mask, yValue, linestyle=linestyle, color=color, linewidth=linewidth)
    elif type_plot == 'hist':
        axs.hist(pattern_for_mask, density=1, linestyle=linestyle, color=color, linewidth=linewidth)
        # axs.plot(bins, linestyle=linestyle, color=color, linewidth=linewidth)
    print(4)
    axs.set_xlabel(xLabel if xLabel else 'default X')
    axs.set_ylabel(yLabel if yLabel else 'default Y')
    axs.grid(grid_mode)
    print(5)
    plt.xticks(pattern_for_mask, xValue, rotation='vertical')
    plt.title(str(sensor_name))
    print(6)
    fig.tight_layout()
    if save_fig:
        print(7)
        plt.savefig('D:\\{}_{}_{}.png'.format(sensor_name, yLabel, time.time()), dpi=1200)
    print(8)
    plt.show(block=True)
    # plt.draw()


def one_plot_for_bot(Value, name, yLabel=None, datetime_mode='time', sensor_name='Unknown', grid_mode=False,
                     type_plot='line', color='cornflowerblue', linestyle='-', linewidth=2, save_fig=True):

    __point_for_save(Value, sensor_name, yLabel)

    xValue, xLabel, pattern_for_mask = _handler_xticks(Value[1], datetime_mode)
    yValue = Value[0]

    fig, axs = plt.subplots()

    if type_plot == 'line':
        axs.plot(pattern_for_mask, yValue, linestyle=linestyle, color=color, linewidth=linewidth)
    elif type_plot == 'hist':
        axs.hist(pattern_for_mask, density=1, linestyle=linestyle, color=color, linewidth=linewidth)
        # axs.plot(bins, linestyle=linestyle, color=color, linewidth=linewidth)

    axs.set_xlabel(xLabel if xLabel else 'default X')
    axs.set_ylabel(yLabel if yLabel else 'default Y')
    axs.grid(grid_mode)

    plt.xticks(pattern_for_mask, xValue, rotation='vertical')
    plt.title(str(sensor_name))

    fig.tight_layout()

    plt.savefig(name, dpi=200)


def two_plot_for_bot(Value_1, Value_2, name, yLabel_1=None, yLabel_2=None, datetime_mode='time', sensor_name='Unknown',
                     grid_mode=False, type_plot='line', color_1='cornflowerblue', color_2='C1', linestyle='-',
                     linewidth=2, save_fig=True):

    xValue_1, xLabel_1, pattern_for_mask_1 = _handler_xticks(Value_1[1], datetime_mode)
    xValue_2, xLabel_2, pattern_for_mask_2 = _handler_xticks(Value_2[1], datetime_mode)
    yValue_1 = Value_1[0]
    yValue_2 = Value_2[0]

    # search min and max
    if yLabel_1 == yLabel_2 and yLabel_1:
        min_value = min(min(yValue_1), min(yValue_2)) - 4
        max_value = max(max(yValue_1), max(yValue_2)) + 4
    else:
        min_value = 0
        max_value = 0

    fig = plt.figure()
    axs = list()

    # First curve
    axs.append(fig.add_subplot(111, label="1"))

    axs[0].plot(pattern_for_mask_1, yValue_1, linestyle=linestyle, color=color_1, linewidth=linewidth)
    if min_value and max_value:
        axs[0].set_ylim(min_value, max_value)
    axs[0].set_ylabel(yLabel_1 if yLabel_1 else 'default Y', color=color_1)
    axs[0].xaxis.set_visible(False)

    # Second curve
    axs.append(fig.add_subplot(111, label="2", frame_on=False))

    axs[1].plot(pattern_for_mask_2, yValue_2, linestyle='-.', color=color_2, linewidth=linewidth)
    if min_value and max_value:
        axs[1].set_ylim(min_value, max_value)
    axs[1].yaxis.tick_right()
    axs[1].set_xlabel(xLabel_2 if xLabel_2 else 'default X')
    axs[1].set_ylabel(yLabel_2 if yLabel_2 else 'default Y', color=color_2)
    axs[1].yaxis.set_label_position('right')

    axs[0].grid(grid_mode)

    plt.xticks(pattern_for_mask_1, xValue_1, rotation='vertical')
    fig.text(0.30, 0.95, sensor_name.split('  ')[0], ha="center", va="bottom", size="medium", color=color_1)
    fig.text(0.5, 0.95, "VS", ha="center", va="bottom", size="medium")
    fig.text(0.70, 0.95, sensor_name.split('  ')[1], ha="center", va="bottom", size="medium", color=color_2)

    fig.tight_layout()

    plt.savefig(name, dpi=200)


def __point_for_save(Value, sensor_name, yLabel):

    data = {'DATA': Value[0], 'TIME': Value[1]}
    f = open('d:/bot_data/data/{}_{}_{}.io'.format(sensor_name, yLabel, time.time()), 'w')
    f.write(str(data))
    f.close()


if __name__ == '__main__':
    one_plot()




