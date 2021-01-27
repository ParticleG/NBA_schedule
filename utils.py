import numpy as np
import pandas as pd

import datetime


def load_data(filename):
    data_frame = pd.read_csv(filename)
    return data_frame


def get_period(start, end):
    return datetime.datetime.strptime(start, '%y/%m/%d') - datetime.datetime.strptime(end, '%y/%m/%d')


def save_to_csv(data, filename):
    header_list = ['GroupNumber',
                   'TotalWinRate',
                   'HostWinRate',
                   'VisitorWinRate',
                   'DatesOfGames',
                   'PeriodsBetweenGames',
                   'AveragePeriodLength',
                   'B2BCounts',
                   'WinningList',
                   'HostingList']
    output_list = []
    for item in data:
        output_list.append(
            {'GroupNumber': item['number'],
             'TotalWinRate': item['total_win_rate'],
             'HostWinRate': item['host_win_rate'],
             'VisitorWinRate': item['visitor_win_rate'],
             'DatesOfGames': item['dates_of_games'],
             'PeriodsBetweenGames': item['periods_between_games'],
             'AveragePeriodLength': item['average_period'],
             'B2BCounts': item['b2b_games'],
             'WinningList': item['is_won'],
             'HostingList': item['is_host']
             }
        )
        data_frame = pd.DataFrame(output_list, columns=header_list)
        data_frame.to_csv(filename, index=False)
