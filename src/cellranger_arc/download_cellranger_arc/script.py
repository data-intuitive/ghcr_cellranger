import random
import time
import os
import re
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

## VIASH START
par = {
  'tag': 'latest',
  'timeout': 600,
  'output': 'cellranger_arc.tar.gz',
  'multiplier': 1.0
}
## VIASH END

url = f"https://support.10xgenomics.com/single-cell-multiome-atac-gex/software/downloads/{par['tag']}"

def sleep(x):
    time.sleep(x * par['multiplier'])

with tempfile.TemporaryDirectory() as download_dir:
    print("Opening Firefox", flush=True)
    options = webdriver.firefox.options.Options()
    options.headless = True
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip,application/x-gzip,application/x-tar")

    driver = webdriver.Firefox(options=options)

    def random_keys():
        return "".join([random.choice('qwertzuiopasdfghjklyxcvbnm') for _ in range(random.randrange(5, 10))])

    sleep(5)

    print("Navigating to form", flush=True)
    driver.get(url)

    sleep(5)

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
    sleep(3)

    # Wait until file is completely downloaded before exiting
    i = 0
    while i < par["timeout"] and os.path.exists(dest_path + ".part"):
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
