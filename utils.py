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
                   'is_b2b': [],

                   '_total_wins': 0,
                   '_total_home_wins': 0,
                   '_total_home_games': 0,
                   '_total_visitor_wins': 0,
                   '_total_visitor_games': 0, } for i in range(30)]
    for index, row in raw_data.iterrows():
        group_list[row['Home']]['dates_of_games'].append(row['Date'])
        group_list[row['Home']]['is_won'].append(row['Winner'] == row['Home'])
        group_list[row['Home']]['is_host'].append(True)
        group_list[row['Home']]['is_b2b'].append(False)
        group_list[row['Home']]['_total_wins'] += row['Winner'] == row['Home']
        group_list[row['Home']]['_total_home_wins'] += row['Winner'] == row['Home']
        group_list[row['Home']]['_total_home_games'] += 1

        group_list[row['Visitor']]['dates_of_games'].append(row['Date'])
        group_list[row['Visitor']]['is_won'].append(row['Winner'] == row['Visitor'])
        group_list[row['Visitor']]['is_host'].append(False)
        group_list[row['Visitor']]['is_b2b'].append(False)
        group_list[row['Visitor']]['_total_wins'] += row['Winner'] == row['Visitor']
        group_list[row['Visitor']]['_total_visitor_wins'] += row['Winner'] == row['Visitor']
        group_list[row['Visitor']]['_total_visitor_games'] += 1

    for group in group_list:
        if group['_total_home_games'] + group['_total_visitor_games'] == 0:
            group['total_win_rate'] = -1
        else:
            group['total_win_rate'] = group['_total_wins'] / (group['_total_home_games'] + group['_total_visitor_games'])

        if group['_total_home_games'] == 0:
            group['host_win_rate'] = -1
        else:
            group['host_win_rate'] = group['_total_home_wins'] / group['_total_home_games']

        if group['_total_visitor_games'] == 0:
            group['visitor_win_rate'] = -1
        else:
            group['visitor_win_rate'] = group['_total_visitor_wins'] / group['_total_visitor_games']

        for i in range(len(group['dates_of_games'])):
            if i == 0:
                group['periods_between_games'].append(0)
            else:
                group['periods_between_games'].append(get_period(group['dates_of_games'][i], group['dates_of_games'][i - 1]).days)

        if len(group['periods_between_games']) == 0:
            group['average_period'] = -1
        else:
            group['average_period'] = np.sum(group['periods_between_games']) / len(group['periods_between_games'])

        for i in range(len(group['periods_between_games'])):
            if i != 0 and group['periods_between_games'][i] == 1:
                if not group['is_host'][i] and not group['is_host'][i - 1]:
                    group['b2b_games'] += 1
                    group['is_b2b'][i] = True

    return group_list


def save_specified_win_rate(group_list, filename):
    header_list = ['GroupNumber',
                   'WinRate_1',
                   'WinRate_2',
                   'WinRate_3',
                   'WinRate_8',
                   'WinRate_9',
                   'WinRate_10',

                   'GameCount_1',
                   'GameCount_2',
                   'GameCount_3',
                   'GameCount_8',
                   'GameCount_9',
                   'GameCount_10']

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
            'WinRate_10': result['win_rate_10'],

            'GameCount_1': result['_game_count_1'],
            'GameCount_2': result['_game_count_2'],
            'GameCount_3': result['_game_count_3'],
            'GameCount_8': result['_game_count_8'],
            'GameCount_9': result['_game_count_9'],
            'GameCount_10': result['_game_count_10']
        })

    data_frame = pd.DataFrame(output_list, columns=header_list)
    data_frame.to_csv(filename, index=False)


def save_b2b_win_rate(group_list, filename):
    header_list = ['GroupNumber',
                   'BothWinRate',
                   'LatterWinRate',

                   '1_AfterWinRate',
                   '1_AfterGameCount',
                   '2_AfterWinRate',
                   '2_AfterGameCount',
                   '3_AfterWinRate',
                   '3_AfterGameCount',
                   '4_AfterWinRate',
                   '4_AfterGameCount',
                   '5_AfterWinRate',
                   '5_AfterGameCount',
                   '6_AfterWinRate',
                   '6_AfterGameCount',
                   '7_AfterWinRate',
                   '7_AfterGameCount',
                   '8_AfterWinRate',
                   '8_AfterGameCount',
                   '9_AfterWinRate',
                   '9_AfterGameCount',
                   '10_AfterWinRate',
                   '10_AfterGameCount',

                   'B2BGameCount',
                   'VisitorWinRate',
                   'TotalWinRate']

    result_list = [{'number': i,
                    'both_win_rate': 0.0,
                    'latter_win_rate': 0.0,
                    'visitor_win_rate': 0.0,
                    'total_win_rate': 0.0,

                    'after_win_rate': [0.0] * 10,
                    'after_game_count': [0] * 10,

                    '_both_win_count': 0,
                    '_latter_win_count': 0,
                    '_b2b_game_count': 0,

                    '_after_win_count': [0] * 10} for i in range(30)]

    output_list = []

    for group in group_list:
        result_list[group['number']]['visitor_win_rate'] = group['visitor_win_rate']
        result_list[group['number']]['total_win_rate'] = group['total_win_rate']
        if group['b2b_games'] == 0:
            result_list[group['number']]['_b2b_game_count'] = -1
        else:
            result_list[group['number']]['_b2b_game_count'] = group['b2b_games'] * 2

        for i in range(len(group['periods_between_games'])):
            if i != 0 and group['is_b2b'][i]:
                if group['is_won'][i - 1]:
                    result_list[group['number']]['_both_win_count'] += 1
                if group['is_won'][i]:
                    result_list[group['number']]['_latter_win_count'] += 1
                    result_list[group['number']]['_both_win_count'] += 1

                for j in range(10):
                    for k in range(j + 1):
                        temp_index = i + k + 1
                        if temp_index >= len(group['periods_between_games']) or group['is_b2b'][temp_index]:
                            break
                        if group['is_won'][temp_index]:
                            result_list[group['number']]['_after_win_count'][j] += 1
                        result_list[group['number']]['after_game_count'][j] += 1

    for result in result_list:
        result['both_win_rate'] = result['_both_win_count'] / result['_b2b_game_count']
        result['latter_win_rate'] = result['_latter_win_count'] / result['_b2b_game_count']
        for i in range(10):
            if result['after_game_count'][i] == 0:
                result['after_win_rate'][i] = -1
            else:
                result['after_win_rate'][i] = result['_after_win_count'][i] / result['after_game_count'][i]
        output_list.append({
            'GroupNumber': result['number'],
            'BothWinRate': result['both_win_rate'],
            'LatterWinRate': result['latter_win_rate'],

            '1_AfterWinRate': result['after_win_rate'][0],
            '1_AfterGameCount': result['after_game_count'][0],
            '2_AfterWinRate': result['after_win_rate'][1],
            '2_AfterGameCount': result['after_game_count'][1],
            '3_AfterWinRate': result['after_win_rate'][2],
            '3_AfterGameCount': result['after_game_count'][2],
            '4_AfterWinRate': result['after_win_rate'][3],
            '4_AfterGameCount': result['after_game_count'][3],
            '5_AfterWinRate': result['after_win_rate'][4],
            '5_AfterGameCount': result['after_game_count'][4],
            '6_AfterWinRate': result['after_win_rate'][5],
            '6_AfterGameCount': result['after_game_count'][5],
            '7_AfterWinRate': result['after_win_rate'][6],
            '7_AfterGameCount': result['after_game_count'][6],
            '8_AfterWinRate': result['after_win_rate'][7],
            '8_AfterGameCount': result['after_game_count'][7],
            '9_AfterWinRate': result['after_win_rate'][8],
            '9_AfterGameCount': result['after_game_count'][8],
            '10_AfterWinRate': result['after_win_rate'][9],
            '10_AfterGameCount': result['after_game_count'][9],

            'B2BGameCount': result['_b2b_game_count'],
            'VisitorWinRate': result['visitor_win_rate'],
            'TotalWinRate': result['visitor_win_rate']
        })

    data_frame = pd.DataFrame(output_list, columns=header_list)
    data_frame.to_csv(filename, index=False)


def save_all_stars(group_list, filename):
    header_list = ['GroupNumber',

                   '5_BeforeHostWinRate',
                   '5_BeforeVisitorWinRate',
                   '5_AfterHostWinRate',
                   '5_AfterVisitorWinRate',

                   '5_BeforeHostWinCount',
                   '5_BeforeVisitorWinCount',
                   '5_AfterHostWinCount',
                   '5_AfterVisitorWinCount',

                   'HostWinRate',
                   'VisitorWinRate',
                   'TotalWinRate']

    result_list = [{'number': i,

                    '5_BeforeHostWinRate': 0.0,
                    '5_BeforeVisitorWinRate': 0.0,
                    '5_AfterHostWinRate': 0.0,
                    '5_AfterVisitorWinRate': 0.0,

                    '5_BeforeHostWinCount': 0,
                    '5_BeforeVisitorWinCount': 0,
                    '5_AfterHostWinCount': 0,
                    '5_AfterVisitorWinCount': 0,

                    'HostWinRate': 0.0,
                    'VisitorWinRate': 0.0,
                    'TotalWinRate': 0.0} for i in range(30)]

    output_list = []

    for group in group_list:
        result_list[group['number']]['HostWinRate'] = group['host_win_rate']
        result_list[group['number']]['VisitorWinRate'] = group['visitor_win_rate']
        result_list[group['number']]['TotalWinRate'] = group['total_win_rate']
        for i in range(len(group['dates_of_games'])):
            if i != 0 and datetime.datetime.strptime(group['dates_of_games'][i], '%y/%m/%d') > datetime.datetime.strptime('19/2/14', '%y/%m/%d'):
                host_game_count = 0
                visitor_game_count = 0

                temp_index = 0
                while host_game_count < 5:
                    temp_index -= 1
                    if group['is_host'][i + temp_index]:
                        host_game_count += 1
                        if group['is_won'][i + temp_index]:
                            result_list[group['number']]['5_BeforeHostWinCount'] += 1

                temp_index = 0
                while visitor_game_count < 5:
                    temp_index -= 1
                    if not group['is_host'][i + temp_index]:
                        visitor_game_count += 1
                        if group['is_won'][i + temp_index]:
                            result_list[group['number']]['5_BeforeVisitorWinCount'] += 1

                host_game_count = 0
                visitor_game_count = 0

                temp_index = 0
                while host_game_count < 5:
                    if group['is_host'][i + temp_index]:
                        host_game_count += 1
                        if group['is_won'][i + temp_index]:
                            result_list[group['number']]['5_AfterHostWinCount'] += 1
                    temp_index += 1

                temp_index = 0
                while visitor_game_count < 5:
                    if not group['is_host'][i + temp_index]:
                        visitor_game_count += 1
                        if group['is_won'][i + temp_index]:
                            result_list[group['number']]['5_AfterVisitorWinCount'] += 1
                    temp_index += 1

                break

    for result in result_list:
        result['5_BeforeHostWinRate'] = result['5_BeforeHostWinCount'] / 5
        result['5_BeforeVisitorWinRate'] = result['5_BeforeVisitorWinCount'] / 5
        result['5_AfterHostWinRate'] = result['5_AfterHostWinCount'] / 5
        result['5_AfterVisitorWinRate'] = result['5_AfterVisitorWinCount'] / 5

        output_list.append({
            'GroupNumber': result['number'],

            '5_BeforeHostWinRate': result['5_BeforeHostWinRate'],
            '5_BeforeVisitorWinRate': result['5_BeforeVisitorWinRate'],
            '5_AfterHostWinRate': result['5_AfterHostWinRate'],
            '5_AfterVisitorWinRate': result['5_AfterVisitorWinRate'],

            '5_BeforeHostWinCount': result['5_BeforeHostWinCount'],
            '5_BeforeVisitorWinCount': result['5_BeforeVisitorWinCount'],
            '5_AfterHostWinCount': result['5_AfterHostWinCount'],
            '5_AfterVisitorWinCount': result['5_AfterVisitorWinCount'],

            'HostWinRate': result['HostWinRate'],
            'VisitorWinRate': result['VisitorWinRate'],
            'TotalWinRate': result['TotalWinRate']
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


def random_swap(raw_data):
    temp_data = raw_data
    first_index = np.random.randint(0, temp_data.shape[0])
    second_index = np.random.randint(0, temp_data.shape[0])
    while second_index == first_index:
        second_index = np.random.randint(0, temp_data.shape[0])

    temp_row = temp_data.loc[first_index]
    temp_data.loc[first_index] = np.hstack([temp_data.loc[first_index][0], temp_data.loc[second_index][1:]])
    temp_data.loc[second_index] = np.hstack([temp_data.loc[second_index][0], temp_row[1:]])

    return temp_data


def check_if_valid(temperature, before_data, after_data):
    before_group_list = calculate_basic_data(before_data)
    after_group_list = calculate_basic_data(after_data)
    before_b2b_count = 0
    after_b2b_count = 0

    for group in before_group_list:
        before_b2b_count += group['b2b_games']

    for group in after_group_list:
        after_b2b_count += group['b2b_games']
        for i in range(len(group['periods_between_games'])):
            if i != 0 and group['periods_between_games'][i] == 1 and group['periods_between_games'][i - 1] == 1:
                print('Invalid attempt: Three continuous games for one group.')
                return temperature, False
            if i > 4 and get_period(group['dates_of_games'][i], group['dates_of_games'][i - 5]).days < 8:
                print(get_period(group['dates_of_games'][i], group['dates_of_games'][i - 5]).days)
                print('Invalid attempt: Five games for one group withing 8 days.')
                return temperature, False

    if after_b2b_count < before_b2b_count:
        print('Valid attempt: Less B2B Count.')
        return temperature * 0.999, True
    else:
        probability = np.exp((0 - (after_b2b_count - before_b2b_count)) / temperature)
        if np.random.rand() > probability:
            print('Invalid attempt: Over probability.')
            return temperature * 0.999, False
    print('Valid attempt: Beyond probability.')
    return temperature * 0.999, True
