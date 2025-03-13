import selenium
import selenium.webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pandas import DataFrame
import os
from datetime import datetime
import sys

# link for the website and path of chromedriver
website = "https://www.thesun.co.uk/"
path = "chromedriver.exe"
application_path = os.path.dirname('main.py')

# headless-mode 
options = Options()
chr_options = selenium.webdriver.ChromeOptions()

chr_options.add_argument('--ignore-certificate-errors')
chr_options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless=new')

# get the HTML of the website
service = Service(executable_path = path)
driver = selenium.webdriver.Chrome(service = service, options = options)
driver.get(website)

# find the heading containers of all the news pages
elements = driver.find_elements(by = 'xpath', value = '//div[@class = "teaser__copy-container"]/a')

# extra variables
titles = []
subtitles = []
links = []

# extract the headline/subheadline of all selected elements
for element in elements:
    try:
        title = element.find_element(by='xpath', value='./span').text
        subtitle = element.find_element(by='xpath', value='./h3').text
        link = element.find_element(by='xpath', value='.').get_attribute('href')
    except:
        pass

    titles.append(title)
    subtitles.append(subtitle)
    links.append(link)

# convert the lists into a dict to turn them into a df
elements_dict = {'titles': titles, 'subtitles': subtitles, 'links':links}
elements_df = DataFrame(elements_dict)

# Add the file's date to file name
now = datetime.now()

dmy_date = now.strftime('%d%m%Y')
file_name = f'headline--{dmy_date}'

# export as csv
final_path = os.path.join(application_path, file_name)
print(final_path)
elements_df.to_csv(final_path)

driver.quit()
