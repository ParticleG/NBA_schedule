import numpy as np
import pandas as pd

import datetime


def load_data(filename):
    data_frame = pd.read_csv(filename)
    return data_frame


def get_period(start, end):
    return datetime.datetime.strptime(start, '%y/%m/%d') - datetime.datetime.strptime(end, '%y/%m/%d')


def calculate_basic_data(raw_data):
    group_list = [{'number': i,
                   'total_win_rate': 0,
                   'host_win_rate': 0,
                   'visitor_win_rate': 0,

                   'dates_of_games': [],
                   'periods_between_games': [],
                   'average_period': 0,

                   'b2b_games': 0,
                   'is_won': [],
                   'is_host': [],

                   '_total_wins': 0,
                   '_total_home_wins': 0,
                   '_total_home_games': 0,
                   '_total_visitor_wins': 0,
                   '_total_visitor_games': 0, } for i in range(30)]
    for index, row in raw_data.iterrows():
        group_list[row['Home']]['dates_of_games'].append(row['Date'])
        group_list[row['Home']]['is_won'].append(row['Winner'] == row['Home'])
        group_list[row['Home']]['is_host'].append(True)
        group_list[row['Home']]['_total_wins'] += row['Winner'] == row['Home']
        group_list[row['Home']]['_total_home_wins'] += row['Winner'] == row['Home']
        group_list[row['Home']]['_total_home_games'] += 1

        group_list[row['Visitor']]['dates_of_games'].append(row['Date'])
        group_list[row['Visitor']]['is_won'].append(row['Winner'] == row['Visitor'])
        group_list[row['Visitor']]['is_host'].append(False)
        group_list[row['Visitor']]['_total_wins'] += row['Winner'] == row['Visitor']
        group_list[row['Visitor']]['_total_visitor_wins'] += row['Winner'] == row['Visitor']
        group_list[row['Visitor']]['_total_visitor_games'] += 1

    for group in group_list:
        group['total_win_rate'] = group['_total_wins'] / (group['_total_home_games'] + group['_total_visitor_games'])
        group['host_win_rate'] = group['_total_home_wins'] / group['_total_home_games']
        group['visitor_win_rate'] = group['_total_visitor_wins'] / group['_total_visitor_games']

        for i in range(len(group['dates_of_games'])):
            if i == 0:
                group['periods_between_games'].append(0)
            else:
                group['periods_between_games'].append(get_period(group['dates_of_games'][i], group['dates_of_games'][i - 1]).days)
        group['average_period'] = np.sum(group['periods_between_games']) / len(group['periods_between_games'])

        for i in range(len(group['periods_between_games'])):
            if i != 0 and group['periods_between_games'][i] == 1:
                if not group['is_host'][i] and not group['is_host'][i - 1]:
                    group['b2b_games'] += 1

    return group_list


def save_specified_win_rate(group_list, filename):
    header_list = ['GroupNumber',
                   'WinRate_1',
                   'WinRate_2',
                   'WinRate_3',
                   'WinRate_8',
                   'WinRate_9',
                   'WinRate_10']

    result_list = [{'number': i,
                    'win_rate_1': 0,
                    'win_rate_2': 0,
                    'win_rate_3': 0,
                    'win_rate_8': 0,
                    'win_rate_9': 0,
                    'win_rate_10': 0,

                    '_win_count_1': 0,
                    '_win_count_2': 0,
                    '_win_count_3': 0,
                    '_win_count_8': 0,
                    '_win_count_9': 0,
                    '_win_count_10': 0,

                    '_game_count_1': 0,
                    '_game_count_2': 0,
                    '_game_count_3': 0,
                    '_game_count_8': 0,
                    '_game_count_9': 0,
                    '_game_count_10': 0, } for i in range(30)]

    output_list = []

    for group in group_list:
        for i in range(len(group['periods_between_games'])):
            if group['periods_between_games'][i] == 1:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_1'] += 1
                result_list[group['number']]['_game_count_1'] += 1
            elif group['periods_between_games'][i] == 2:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_2'] += 1
                result_list[group['number']]['_game_count_2'] += 1
            elif group['periods_between_games'][i] == 3:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_3'] += 1
                result_list[group['number']]['_game_count_3'] += 1
            elif group['periods_between_games'][i] == 8:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_8'] += 1
                result_list[group['number']]['_game_count_8'] += 1
            elif group['periods_between_games'][i] == 9:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_9'] += 1
                result_list[group['number']]['_game_count_9'] += 1
            elif group['periods_between_games'][i] == 10:
                if group['is_won'][i]:
                    result_list[group['number']]['_win_count_10'] += 1
                result_list[group['number']]['_game_count_10'] += 1

    for result in result_list:
        if result['_game_count_1'] == 0:
            result['win_rate_1'] = -1
        else:
            result['win_rate_1'] = result['_win_count_1'] / result['_game_count_1']

        if result['_game_count_2'] == 0:
            result['win_rate_2'] = -1
        else:
            result['win_rate_2'] = result['_win_count_2'] / result['_game_count_2']

        if result['_game_count_3'] == 0:
            result['win_rate_3'] = -1
        else:
            result['win_rate_3'] = result['_win_count_3'] / result['_game_count_3']

        if result['_game_count_8'] == 0:
            result['win_rate_8'] = -1
        else:
            result['win_rate_8'] = result['_win_count_8'] / result['_game_count_8']

        if result['_game_count_9'] == 0:
            result['win_rate_9'] = -1
        else:
            result['win_rate_9'] = result['_win_count_9'] / result['_game_count_9']

        if result['_game_count_10'] == 0:
            result['win_rate_10'] = -1
        else:
            result['win_rate_10'] = result['_win_count_10'] / result['_game_count_10']

        output_list.append({
            'GroupNumber': result['number'],
            'WinRate_1': result['win_rate_1'],
            'WinRate_2': result['win_rate_2'],
            'WinRate_3': result['win_rate_3'],
            'WinRate_8': result['win_rate_8'],
            'WinRate_9': result['win_rate_9'],
            'WinRate_10': result['win_rate_10']
        })

    data_frame = pd.DataFrame(output_list, columns=header_list)
    data_frame.to_csv(filename, index=False)


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
