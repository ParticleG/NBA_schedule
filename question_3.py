from utils import *

if __name__ == '__main__':
    raw_data = load_data("2018-2019.csv")
    temperature = 1.0
    while temperature > 1.0e-30:
        print(f'temperature: {temperature}')
        after_raw_data = random_swap(raw_data)
        temperature, is_valid = check_if_valid(temperature, raw_data, after_raw_data)
        if is_valid:
            raw_data = after_raw_data
    pd.save_to_csv(raw_data, '2018-2019_annealed.csv')
