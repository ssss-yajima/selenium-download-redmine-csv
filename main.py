import os
import yaml
import csv
from datetime import datetime as dt

from redmine_download_query import RedmineQueryParam, MyRedmineDriver

if __name__ == '__main__':

    # read login params
    with open("params.yaml", "r") as yml:
        params = yaml.safe_load(yml)
    redmine_url = params['redmine']['url']
    redmine_user_id = params['redmine']['user_id']

    print('Login to Redmine(%s) as %s.' % (redmine_url, redmine_user_id))
    print('Redmine password > ', end='')
    redmine_password = input()

    # other settings
    redmine_dir = os.path.join(os.getcwd(), 'redmine')
    exec_datetime = dt.now()

    # read queries
    print('Read target projects from queries.csv')
    with open("queries.csv", "r") as f:
        reader = csv.DictReader(f)
        queries = [
            RedmineQueryParam(row['project_id'], row['query_id'])
            for row in reader
        ]

    # download from redmine
    print('Download from Redmine.')
    my_driver = MyRedmineDriver(base_url=redmine_url,
                                output_dir=redmine_dir,
                                exec_datetime=exec_datetime)
    my_driver.init_chrome_driver()
    my_driver.login_redmine(redmine_user_id, redmine_password)
    my_driver.download_query_csv_filses(queries)

    print('Done!')
