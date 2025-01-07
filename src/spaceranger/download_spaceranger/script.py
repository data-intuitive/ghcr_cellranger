import random
import time
import os
import re
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import sys
from pathlib import Path

debug = False
## VIASH START
par = {
  'tag': 'latest',
  'timeout': 600,
  'output': 'spaceranger.tar.gz',
  'multiplier': 1.0
}
debug=True
## VIASH END

if par['gh_token']:
    os.environ['GH_TOKEN'] = par['gh_token']

url = "https://www.10xgenomics.com/support/software/space-ranger/downloads/previous-versions"

major, _, minor_and_other = par['tag'].partition('.')
minor = ""
if major != "latest":
    minor, _, _ = minor_and_other.partition('.')
    major_str=f" {major}."
else:
    major_str=""


def sleep(x):
    time.sleep(x * par['multiplier'])

def is_download_finished(temp_folder):
    firefox_temp_file = sorted(Path(temp_folder).glob('*.part'))
    chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    downloaded_files = sorted(Path(temp_folder).glob('*.*'))
    if (len(firefox_temp_file) == 0) and \
    (len(chrome_temp_file) == 0) and \
    (len(downloaded_files) >= 1):
        return True
    else:
        return False

# download_dir = tempfile.TemporaryDirectory().name
with tempfile.TemporaryDirectory() as download_dir:
    print("Opening Firefox", flush=True)
    options = webdriver.firefox.options.Options()
    if not debug:
        options.add_argument("-headless") 
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip,application/x-gzip,application/x-tar")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)  

    def random_keys():
        return "".join([random.choice('qwertzuiopasdfghjklyxcvbnm') for _ in range(random.randrange(5, 10))])

    sleep(5)
    print("Navigating to form", flush=True)
    driver.get(url)
    delay = 25
    try:
        WebDriverWait(driver, 25).until(expected_conditions.presence_of_element_located((By.ID, 'FirstName'))) 
    except TimeoutException as e:
        raise e
    # Fill out form
    driver.find_element(By.ID, 'FirstName').send_keys(random_keys())
    sleep(.1)
    driver.find_element(By.ID, 'LastName').send_keys(random_keys())
    sleep(.1)
    driver.find_element(By.ID, 'Email').send_keys(random_keys() + '@gmail.com')
    sleep(.1)
    driver.find_element(By.ID, 'Company').send_keys(random_keys())
    select = Select(driver.find_element(By.ID, 'Country'))
    select.select_by_index(1)
    sleep(.1)
    try:
        driver.find_element(By.ID, 'PostalCode').send_keys(random_keys())
    except NoSuchElementException:
        pass

    select = Select(driver.find_element(By.ID, 'tempIndustry'))
    select.select_by_index(1)
    sleep(.1)
    select = Select(driver.find_element(By.ID, 'Primary_Area_of_Research__c'))
    select.select_by_index(1)
    sleep(.1)
    checkbox = driver.find_element(By.ID, "collectionConsent").find_element(By.XPATH, "preceding-sibling::*")
    assert "Box" in checkbox.get_attribute("Class")
    checkbox.click()
    assert driver.find_element(By.ID, "collectionConsent").get_attribute("checked") == "true"
    
    # Go to download page
    print("Navigating to download page", flush=True)
    driver.find_element(By.TAG_NAME, "form").submit()
    sleep(8)

    # Download spaceranger
    print("Downloading SpaceRanger", flush=True)
    elem = driver.find_element(By.XPATH, f"//*[contains(., 'Space Ranger{major_str}{minor}')]/following-sibling::div//*[text()[contains(.,'Download for Linux 64-bit (tar.gz)')]]/parent::a")
    elem.click()
    url = elem.get_property("href")
    filename = re.sub("^.*/([^?/]*)?[^/]*$", "\\1", url)
    dest_path = os.path.join(download_dir, filename)
    sleep(3)

    # Wait until file is completely downloaded before exiting
    i = 0
    while i < par["timeout"] and not is_download_finished(download_dir):
        sleep(3)
        print("Content of download dir: " + ', '.join(os.listdir(download_dir)), flush=True)
        i += 1

    print("Quitting firefox", flush=True)
    driver.quit()

    files = os.listdir(download_dir)

    if is_download_finished(download_dir) and len(files) != 1:
        print("Content of download dir: " + ', '.join(files), flush=True)
        raise FileNotFoundError(f"Download has not completed after {par['timeout']}s. Is this script still working?")

    dest_path = files[0]

    print(f"Copying {dest_path} to {par['output']}", flush=True)
    shutil.copy(os.path.join(download_dir, dest_path), par["output"])

    print("Download complete", flush=True)
    sys.stdout.flush()
