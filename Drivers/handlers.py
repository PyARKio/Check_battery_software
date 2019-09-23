# -- coding: utf-8 --
from __future__ import unicode_literals
from multiprocessing import Process
import sys


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


"""
IN CLASS 681970459visualization-p1c @00124b001d03101d_climate #type_data=battery #save_fig=true
00124b001d03101d_climate
{'type_data': 'battery', 'save_fig': 'true'}
00124b001d03101d climate
[[2.880000114440918, 2.880000114440918], ['2019-09-23 07:22:59', '2019-09-23 07:23:59']]
"""


def _handler_plot_data_for_bot(self, request):
    """

    :param request:
    :return:
    """
    if '@' in request:
        sType = request.split(' @')[1].split(' ')[0].lower()

        # all params for ploting in dict type
        try:
            ploting_params = dict(tuple(x.split('=')) for x in request.split(sType)[1].split(' #')[1::])
        except:
            sys.stdout.write('\nAll params must have their value\nTry again\n')
            return 0

        if not ploting_params.get('type_data'):
            sys.stdout.write('\nEnter "type_data"\nTry again\n')
            return 0

        try:
            key_name = self.ploting_params_dict_for_bot[ploting_params.get('type_data')](self, sType, ploting_params)
        except:
            sys.stdout.write('\nEnter correct value for "type_data"\nTry again\n')
            return 0
        else:
            return key_name
    else:
        sys.stdout.write('\nIn line empty type sensor!\nTry again\n')

        return 0


def _is_cmd_battery_for_bot(self, sType_raw, params):
    print(sType_raw)
    print(params)

    sType = '{} {}'.format(sType_raw.split('_')[0], sType_raw.split('_')[1])
    print(sType)
    print(self.work_object.table_of_handlers[sType.split(' ')[1]].sensors_battery[sType])

    if True:
        key_name = 'D:/bot_graph/{}_{}_{}.png'.format(sType, params['type_data'], time.time())
        plot_start = Process(target=one_plot_for_bot,
                             args=(self.work_object.table_of_handlers[sType.split(' ')[1]].sensors_battery[sType],
                                   key_name,
                                   params['type_data'].upper(),
                                   'time' if params.get('datetime_mode') is None else params['datetime_mode'],
                                   sType,
                                   False if params.get('grid') is None else params['grid'],
                                   'line' if params.get('type_plot') is None else params['type_plot'],
                                   'cornflowerblue' if params.get('color') is None else params['color'],
                                   '-' if params.get('linestyle') is None else params['linestyle'],
                                   2 if params.get('linewidth') is None else params['linewidth'],
                                   False if params.get('save_fig') is None else params['save_fig'],

                                   ))
        plot_start.start()
        return key_name
