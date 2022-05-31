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
  'timeout': 600,
  'output': 'bcl-convert.rpm',
  'email': 'foo',
  'password': 'bar',
  'multiplier': 1.0
}
## VIASH END

url = "https://emea.support.illumina.com/sequencing/sequencing_software/bcl-convert/downloads.html"

def sleep(x):
    time.sleep(x * par['multiplier'])

with tempfile.TemporaryDirectory() as download_dir:
    print("Opening Firefox", flush=True)
    options = webdriver.firefox.options.Options()
    options.headless = True
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")

    driver = webdriver.Firefox(options=options)

    sleep(2)

    print("Navigating to page", flush=True)
    driver.get(url)
    sleep(5)

    print("Clicking trust policy", flush=True)
    elem = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    elem.click()
    sleep(5)
    print("View options", flush=True)
    elem = driver.find_element(By.PARTIAL_LINK_TEXT, "View Options")
    elem.click()
    sleep(5)

    print("Clicking url", flush=True)
    elem = driver.find_element(By.PARTIAL_LINK_TEXT, "(RPM format)")
    url = elem.get_property("href")
    f1 = re.sub("^.*assetDetails=([^?/]*.rpm).*$", "\\1", url)
    filename = re.sub("^.*(bcl-convert.*)$", "\\1", f1)
    print(filename, flush=True)
    dest_path = os.path.join(download_dir, filename)
    print(dest_path, flush=True)
    elem.click()
    sleep(20)

    print("Fill in login form", flush=True)
    form = driver.find_element(By.NAME, 'signinForm')
    sleep(.1)
    form.find_element(By.ID, 'login').send_keys(par["email"])
    sleep(.1)
    form.find_element(By.NAME, 'password').send_keys(par["password"])
    sleep(.1)

    print("Downloading file", flush=True)
    form.submit()
    sleep(20)

    print("Waiting until download is complete", flush=True)
    i = 0
    while i < par["timeout"] and os.path.exists(dest_path + ".part"):
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
