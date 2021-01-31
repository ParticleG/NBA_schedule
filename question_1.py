from utils import *

if __name__ == '__main__':
    first_year_raw_data = load_data("2018-2019.csv")
    second_year_raw_data = load_data("2019-2020.csv")

    first_year_group_list = calculate_basic_data(first_year_raw_data)
    second_year_group_list = calculate_basic_data(first_year_raw_data)

    save_specified_win_rate(first_year_group_list, '2018-2019_specified.csv')
    save_specified_win_rate(second_year_group_list, '2019-2020_specified.csv')
    save_b2b_win_rate(first_year_group_list, '2018-2019_b2b.csv')
    save_b2b_win_rate(second_year_group_list, '2019-2020_b2b.csv')
    save_all_stars(first_year_group_list, '2018-2019_allStars.csv')
    save_all_stars(second_year_group_list, '2019-2020_allStars.csv')
    save_to_csv(first_year_group_list, '2018-2019_processed.csv')
    save_to_csv(second_year_group_list, '2019-2020_processed.csv')
