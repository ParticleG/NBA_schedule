from utils import *

if __name__ == '__main__':
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
    # raw_data = load_data("2018-2019.csv")
    raw_data = load_data("2019-2020.csv")
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

    # save_to_csv(group_list, '2018-2019_processed.csv')
    save_to_csv(group_list, '2019-2020_processed.csv')
