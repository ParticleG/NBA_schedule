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
    first_year, second_year = load_data()
    for index, row in first_year.iterrows():
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
        group['total_win_rate'] = group['_total_wins'] / first_year.shape[0]
        group['host_win_rate'] = group['_total_home_wins'] / group['_total_home_games']
        group['visitor_win_rate'] = group['_total_visitor_wins'] / group['_total_visitor_games']
    print(group_list)
