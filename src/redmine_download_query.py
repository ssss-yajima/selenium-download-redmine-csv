import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime as dt


class RedmineQueryParam:
    def __init__(self, project_id, query_id):
        self.project_id = project_id
        self.query_id = query_id


class MyRedmineDriver:
    # constructor
    def __init__(self, base_url, output_base_dir):
        ## yyyymmdd_hhmmss
        self.timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
        self.base_url = base_url
        # create timestamp dir to as output dir
        self.output_dir = os.path.join(output_base_dir, self.timestamp)
        self.driver = None
        self.logged_in = False

    # Quit driver on deconstractor
    def __del__(self):
        if self.driver == None:
            return
        self.driver.quit()
        print('>> Quit driver.')

    def init_chrome_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs", {"download.default_directory": self.output_dir})
        self.driver = webdriver.Chrome(options=options)
        print('>> Initializing chrome driver.')

    def login_redmine(self, id, password):
        if self.driver == None:
            print(
                '>> Driver is not initialized. Call "init_chrome_driver" method first.'
            )
            return
        # login
        self.driver.get(self.base_url + '/login')

        id_box = self.driver.find_element_by_id('username')
        id_box.send_keys(id)
        pass_box = self.driver.find_element_by_id('password')
        pass_box.send_keys(password)

        pass_box.submit()
        print('>> Login to ' + self.base_url)

        try:
            self.driver.find_element_by_id('loggedas')
            self.logged_in = True
        except NoSuchElementException:
            print('>> [ERROR] Failed to login.')
            return

    def download_query_csv_filses(self, redmine_query_params):
        if not self.logged_in:
            print(
                '>> [ERROR] Not authorized. Call "login_redmine" method to login.'
            )
            return

        print('>> Downloading...')
        print('>> Output dir :%s' % self.output_dir)

        for param in redmine_query_params:
            project_url = self.base_url + '/projects/' + param.project_id
            # open query page
            self.driver.get(project_url + '/issues?query_id=' + param.query_id)
            project_name = self.driver.find_element_by_class_name(
                'current-project').text
            query_name = self.driver.find_element_by_tag_name('h2').text

            print('>> Downloading project [%s] with query [%s]' %
                  (project_name, query_name))
            # download csv
            self.driver.get(project_url + '/issues.csv?query_id=' +
                            param.query_id)
            # waiting for download
            download_file_path = os.path.join(self.output_dir, 'issues.csv')
            while (not os.path.exists(download_file_path)):
                time.sleep(1)

            # rename issue.csv to project_name.csv
            filename = '%s_%s.csv' % (project_name, query_name)
            reanamed_file_path = os.path.join(self.output_dir, filename)
            os.rename(download_file_path, reanamed_file_path)


if __name__ == '__main__':
    redmine_url = 'https://my.redmine.jp/demo/'
    download_dir = os.path.join(os.getcwd(), 'redmine_csv')

    # read setting file
    print('> Read target projects from redmine_queries.csv')
    query_params = []
    query_params.append(RedmineQueryParam(project_id='demo', query_id='807'))
    query_params.append(RedmineQueryParam(project_id='demo', query_id='811'))

    user_id = 'developer'
    password = 'developer'

    my_driver = MyRedmineDriver(redmine_url, download_dir)
    my_driver.init_chrome_driver()
    my_driver.login_redmine(user_id, password)
    my_driver.download_query_csv_filses(query_params)

    print('> Done!')
