import time
import os
import re
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import sys
from pathlib import Path

debug = False
## VIASH START
par = {
  'timeout': 600,
  'output': 'bcl-convert.rpm',
  'email': "***REMOVED***",
  'password': "***REMOVED***",
  'multiplier': 1.0,
  'tag': '4.1.5'
}
debug = True
## VIASH END

url = "https://emea.support.illumina.com/sequencing/sequencing_software/bcl-convert/downloads.html"

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

# From https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox
def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

# download_dir = tempfile.TemporaryDirectory().name
with tempfile.TemporaryDirectory() as download_dir:
    print("Opening Firefox", flush=True)
    options = webdriver.firefox.options.Options()
    if not debug:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-rpm")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)  
    sleep(2)

    print("Navigating to page", flush=True)
    driver.get(url)
    sleep(5)

    # print("Clicking trust policy", flush=True)
    # elem = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    # elem.click()
    # sleep(5)

    print("View options", flush=True)
    if par['tag'] != "latest":
        elem = driver.find_element(By.XPATH, f"//*[contains(text(),'BCL Convert v{par['tag']} Installer')]/following-sibling::div[contains(@class, 'show-hide-trigger')]/a")
        scroll_shim(driver, elem)
        webdriver.ActionChains(driver)\
            .scroll_to_element(elem)\
            .perform()
        sleep(5)
    else:
        elem = driver.find_element(By.PARTIAL_LINK_TEXT, "View Options")
    
    elem.click()
    sleep(5)

    print("Clicking url", flush=True)
    if par['tag'] != "latest":
        elem = driver.find_element(By.XPATH, f'//a[contains(@href, ".rpm") and contains(@href, "{par["tag"]}")]')
    else:
        elem = driver.find_element(By.XPATH, '//a[contains(@href, ".rpm")]')


    url = elem.get_property("href")
    f1 = re.sub("^.*assetDetails=([^?/]*.rpm).*$", "\\1", url)
    filename = re.sub("^.*(bcl-convert.*)$", "\\1", f1)
    dest_path = os.path.join(str(download_dir), filename)

    print(f"filename: {filename}")
    print(f"dest_path: {dest_path}")
    try:
        elem.click()
    except ElementClickInterceptedException:
        webdriver.ActionChains(driver)\
            .scroll_to_element(elem)\
            .perform()
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
    

    print("Waiting until download is complete", flush=True)
    i = 0
    while i < par["timeout"] and not is_download_finished(download_dir):
        sleep(1)
        print("Content of download dir: " + ', '.join(os.listdir(download_dir)), flush=True)
        i += 1

    print("Content of download dir: " + ', '.join(os.listdir(download_dir)), flush=True)
    
    print("Quitting firefox", flush=True)
    driver.quit()

    if not os.path.exists(dest_path):
        raise FileNotFoundError(f"Download has not completed after {par['timeout']}s. Is this script still working?")

    print(f"Copying {dest_path} to {par['output']}", flush=True)
    shutil.copy(dest_path, par["output"])

    print("Download complete", flush=True)
    sys.stdout.flush()
