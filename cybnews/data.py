#!/usr/bin/env python3

import pandas as pd
from pathlib import Path
from os.path import abspath


def get_data():
    """
    This function returns a Python dict.
    Its keys should be 'sellers', 'orders', 'order_items' etc...
    Its values should be pandas.DataFrames loaded from csv files
    """
    data = {}

    project_path = Path(abspath(__file__)).parent.parent
    csv_path = project_path.joinpath('data', 'WELFake_Dataset.csv')

    return pd.read_csv(csv_path)


if __name__ == '__main__':
    get_data()
