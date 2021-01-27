from utils import *

if __name__ == '__main__':
    # raw_data = load_data("2018-2019.csv")
    raw_data = load_data("2019-2020.csv")

    group_list = calculate_basic_data(raw_data)

    # save_specified_win_rate(group_list, '2018-2019_specified.csv')
    save_specified_win_rate(group_list, '2019-2020_specified.csv')
    # save_to_csv(group_list, '2018-2019_processed.csv')
    save_to_csv(group_list, '2019-2020_processed.csv')
