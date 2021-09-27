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
    def __init__(self, base_url, output_dir):
        ## yyyymmdd_hhmmss
        self.base_url = base_url
        self.output_dir = output_dir
        self.driver = None
        self.logged_in = False
        self.log_head = 'Redmine'

    # Quit driver on deconstractor
    def __del__(self):
        if self.driver == None:
            return
        self.driver.quit()

    def init_chrome_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs", {"download.default_directory": self.output_dir})
        self.driver = webdriver.Chrome(options=options)
        self.log('Initializing chrome driver.')

    def login_redmine(self, id, password):
        if self.driver == None:
            self.log('Driver is not initialized. Call "init_chrome_driver".')
            return
        # login
        self.driver.get(self.base_url + '/login')

        id_box = self.driver.find_element_by_id('username')
        id_box.send_keys(id)
        pass_box = self.driver.find_element_by_id('password')
        pass_box.send_keys(password)

        pass_box.submit()
        self.log('Login to ' + self.base_url)

        try:
            self.driver.find_element_by_id('loggedas')
            self.logged_in = True
        except NoSuchElementException:
            self.log('[ERROR] Failed to login.')
            return

    def download_query_csv_filses(self, redmine_query_params):
        if not self.logged_in:
            self.log('[ERROR] Not authorized. Call "login_redmine".')
            return
        for param in redmine_query_params:
            project_url = self.base_url + '/projects/' + param.project_id
            # open query page
            self.driver.get(project_url + '/issues?query_id=' + param.query_id)
            project_name = self.driver.find_element_by_class_name(
                'current-project').text
            query_name = self.driver.find_element_by_tag_name('h2').text

            self.log('Downloading project [%s] with query [%s]' %
                     (project_name, query_name))
            # download csv
            self.driver.get(project_url + '/issues.csv?query_id=' +
                            param.query_id)
            # waiting for download
            download_file_path = os.path.join(self.output_dir, 'issues.csv')
            while (not os.path.exists(download_file_path)):
                time.sleep(1)

            # rename issue.csv to {project}_{query}.csv
            filename = '%s_%s.csv' % (project_name, query_name)
            reanamed_file_path = os.path.join(self.output_dir, filename)
            os.rename(download_file_path, reanamed_file_path)

        self.log('Output dir :%s' % self.output_dir)

    def log(self, str):
        # e.g. <Redmine>message
        print("<%s>%s" % (self.log_head, str))
