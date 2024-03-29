import random
import time
import os
import re
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import sys
from pathlib import Path

debug = False
## VIASH START
par = {
  'tag': '2.0',
  'timeout': 600,
  'output': 'cellranger_arc.tar.gz',
  'multiplier': 1.0
}
debug = True
## VIASH END

url = f"https://support.10xgenomics.com/single-cell-multiome-atac-gex/software/downloads/{par['tag']}"

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
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip,application/x-gzip,application/x-tar")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    def random_keys():
        return "".join([random.choice('qwertzuiopasdfghjklyxcvbnm') for _ in range(random.randrange(5, 10))])

    sleep(5)

    print("Navigating to form", flush=True)
    driver.get(url)

    sleep(10)

    # Fill out form
    form = driver.find_element(By.ID, 'eula-form')
    sleep(.1)
    form.find_element(By.ID, 'first_name').send_keys(random_keys())
    sleep(.1)
    form.find_element(By.ID, 'last_name').send_keys(random_keys())
    sleep(.1)
    form.find_element(By.ID, 'email').send_keys(random_keys() + '@gmail.com')
    sleep(.1)
    form.find_element(By.ID, 'company').send_keys(random_keys())
    sleep(.1)
    agree = form.find_element(By.ID, "agree")
    if not agree.is_selected():
        agree.click()

    assert agree.is_selected()

    # Go to download page
    print("Navigating to download page", flush=True)
    form.submit()
    sleep(5)

    # Download cellranger_arc
    print("Downloading Cell Ranger ARC", flush=True)
    elem = driver.find_element(By.PARTIAL_LINK_TEXT, "Linux 64-bit")
    elem.click()
    url = elem.get_property("href")
    filename = re.sub("^.*/([^?/]*)?[^/]*$", "\\1", url)
    dest_path = os.path.join(download_dir, filename)
    dest_path = str(Path(dest_path).with_suffix('.tar'))
    sleep(3)

    # Wait until file is completely downloaded before exiting
    i = 0
    while i < par["timeout"] and not is_download_finished(download_dir):
        sleep(3)
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
