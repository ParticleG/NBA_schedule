import numpy as np
import pandas as pd


def load_data():
    first_year = pd.read_csv("2018-2019.csv")
    second_year = pd.read_csv("2019-2020.csv")
    return first_year, second_year
