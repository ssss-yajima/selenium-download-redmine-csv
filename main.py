import os
import yaml
import csv
from datetime import datetime as dt

from redmine_driver import RedmineQueryParam, MyRedmineDriver
from concat_csv import concat_csv


# read queries.yaml to dict
def read_queries():
    print('Read target projects from queries.csv')
    with open("queries.csv", "r") as f:
        reader = csv.DictReader(f)
        queries = [
            RedmineQueryParam(row['project_id'], row['query_id'])
            for row in reader
        ]
    return queries


def download_redmine(output_dir, params, queries, password):
    print('Download from Redmine.')
    my_driver = MyRedmineDriver(base_url=params['redmine']['url'],
                                output_dir=output_dir)
    my_driver.init_chrome_driver()
    my_driver.login_redmine(id=params['redmine']['user_id'], password=password)
    my_driver.download_query_csv_filses(queries)


if __name__ == '__main__':
    # read login params
    with open("params.yaml", "r") as yml:
        params = yaml.safe_load(yml)

    # input password
    print('Login to Redmine(%s) as %s.' %
          (params['redmine']['url'], params['redmine']['user_id']))
    print('Redmine password > ', end='')
    redmine_password = input()

    # output directory path
    redmine_dir = os.path.join(os.getcwd(), 'redmine',
                               dt.now().strftime('%Y%m%d_%H%M%S'))
    # read queries.yaml
    queries = read_queries()
    # download from redmine
    download_redmine(output_dir=redmine_dir,
                     params=params,
                     queries=queries,
                     password=redmine_password)
    concat_csv(directory_path=redmine_dir,
               encoding=params['redmine']['encoding'])

    print('Done!')
