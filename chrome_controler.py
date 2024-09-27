
import os
"""
try:
    os.system('/usr/bin/google-chrome-stable --start-fullscreen https://staging-retail.calimaco.com/') 
except Exception as e:
    print("Orror opening browser" + str(e))
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome()

driver.get("https://python.org")
print(driver.title)
driver.close()