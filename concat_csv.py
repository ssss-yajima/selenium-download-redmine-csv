import glob
import os

import pandas as pd


def concat_csv(directory_path, encoding):

    filename = 'concat.csv'
    file_path = os.path.join(directory_path, filename)

    # delete existing file
    if os.path.exists(file_path):
        os.remove(file_path)

    files = sorted(glob.glob(os.path.join(directory_path, '*.csv')))
    csv_list = []
    for file in files:
        csv = pd.read_csv(file, encoding=encoding)
        csv_list.append(csv)
        # print(csv)
    merge_csv = pd.concat(csv_list)
    # print(merge_csv)
    merge_csv.to_csv(file_path, encoding=encoding, index=False)
    print('Concatenated csv files -> ' + file_path)


if __name__ == '__main__':
    concat_csv('test', 'UTF-8')
