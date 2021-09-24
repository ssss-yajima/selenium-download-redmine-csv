import time
import os
from selenium import webdriver
from datetime import datetime as dt

# specify download directory
timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
download_dir = os.path.join(os.getcwd(), 'redmine_csv', timestamp)
print('Downloading csv files to:' + download_dir)

# init chromedriver
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",
                                {"download.default_directory": download_dir})
driver = webdriver.Chrome(options=options)

# login
base_url = 'https://my.redmine.jp/demo'
driver.get(base_url + '/login')

id_box = driver.find_element_by_id('username')
id_box.send_keys('developer')
pass_box = driver.find_element_by_id('password')
pass_box.send_keys('developer')

pass_box.submit()

# open query page
project_id = 'demo'
query_id = '807'
driver.get(base_url + '/projects/' + project_id + '/issues?query_id=' +
           query_id)
# get project name
project_name = driver.find_element_by_class_name('current-project').text
print('Downloading... ' + project_name)

# download csv
driver.get(base_url + '/projects/' + project_id + '/issues.csv?query_id=' +
           query_id)

# waiting for download
download_file_path = os.path.join(download_dir, 'issues.csv')
while (not os.path.exists(download_file_path)):
    time.sleep(1)

# rename issue.csv to project_name.csv
reanamed_file_path = os.path.join(download_dir, project_name + '.csv')
os.rename(download_file_path, reanamed_file_path)
# print('Downloaded csv file :' + reanamed_name)

driver.quit()
print('--------------- done ---------------')
