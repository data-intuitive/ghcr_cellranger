import time
import os
import re
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException

import sys
from pathlib import Path

debug = False
## VIASH START
par = {
  'timeout': 600,
  'output': 'bcl2fastq2.zip',
  'email': os.getenv("ILLUMINA_ACCOUNT"),
  'password': os.getenv("ILLUMINA_PASS"),
  'multiplier': 1.0
}
debug = True
## VIASH END

url = "https://emea.support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html"

if par['gh_token']:
    os.environ['GH_TOKEN'] = par['gh_token']

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

with tempfile.TemporaryDirectory() as download_dir:
    print("Opening Firefox", flush=True)
    options = webdriver.firefox.options.Options()
    if not debug:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)  
    sleep(2)

    print("Navigating to page", flush=True)
    driver.get(url)
    sleep(5)
    
    try:
        print("Clicking trust policy", flush=True)
        elem = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        elem.click()
        sleep(5)
    except NoSuchElementException:
        pass


    print("Clicking url", flush=True)
    elem = driver.find_element(By.PARTIAL_LINK_TEXT, "(Linux rpm)")
    url = elem.get_property("href")
    filename = re.sub("^.*assetDetails=([^?/]*.zip).*$", "\\1", url)
    dest_path = os.path.join(download_dir, filename)
    elem.click()
    sleep(20)

    print("Fill in login form", flush=True)
    try:
        form = driver.find_element(By.NAME, 'signinForm')
        sleep(.1)
        form.find_element(By.ID, 'login').send_keys(par["email"])
        sleep(.1)
        form.find_element(By.NAME, 'password').send_keys(par["password"])
        sleep(.1)
        print("Downloading file", flush=True)
        form.submit()
        sleep(10)
    except NoSuchElementException:
        pass
    sleep(20)

    print("Waiting until download is complete", flush=True)
    i = 0
    while i < par["timeout"] and not is_download_finished(download_dir):
        sleep(1)
        print("Content of download dir: " + ', '.join(os.listdir(download_dir)), flush=True)
        i += 1

    print("Quitting firefox", flush=True)
    driver.quit()

    if not os.path.exists(dest_path):
        raise FileNotFoundError(f"Download has not completed after {par['timeout']}s. Is this script still working?")

    print(f"Copying {dest_path} to {par['output']}", flush=True)
    shutil.copy(dest_path, par["output"])

    print("Download complete", flush=True)
    sys.stdout.flush()
