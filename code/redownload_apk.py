from selenium import webdriver
import os
import re
import shutil
import time
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': "D:\\apk_pure\\temp",
    'safebrowsing.enabled': 'false',
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


def get_stored_dir():
    return "D:\\apk_pure\\download"


def get_download_dir():
    return "D:\\apk_pure\\temp"


def download_apk(url):
    if url != "":
        driver.get(url)
        file_name = re.sub(r" \(\d+\.?\d* MB\)", "", driver.find_element_by_class_name("file").text)

        download_count = 0
        while not check_finished(file_name):

            print("downloading %s" % file_name)
            time.sleep(3)

            download_count = download_count + 1
            if download_count >= 60:
                print("{+} download time out")
                return
        print("{+} download %s success" % file_name)
        move_apk(file_name)
    else:
        print("{+} no valid url provided")


def check_finished(apk_name):
    download_dir = get_download_dir()
    apk_file_path = os.path.join(download_dir, apk_name)
    if os.path.isfile(apk_file_path):
        return True
    return False


def move_apk(apk_name):
    download_dir = get_download_dir()
    download_path = os.path.join(download_dir, apk_name)
    stored_dir = get_stored_dir()

    if os.path.isdir(stored_dir) and os.path.isfile(download_path):
        if os.path.exists(os.path.join(stored_dir, apk_name)):
            os.remove(os.path.join(stored_dir, apk_name))
        shutil.move(download_path, stored_dir)


if __name__ == "__main__":
    current_task = "Business Card Maker Visiting Card Maker"
    f = False
    for file in os.listdir(get_stored_dir()):
        if current_task in file:
            f = True
        if file.endswith(".xapk") and f:
            app_name = file.split('.xapk')[0].split("_")[0]

            flag = False
            for _ in os.listdir(get_stored_dir()):
                if app_name in _ and ".apk" in _:
                    flag = True
                    break

            if flag:
                continue

            driver.get("https://apkpure.com/search?q=%s" % app_name)
            try:
                apk_detail_url = driver.find_element_by_tag_name("p>a").get_attribute('href')
            except NoSuchElementException:
                print("{+} no result find in apk pure ")
                continue
            driver.get(apk_detail_url + "/versions")

            if "Page Deleted or Gone" in driver.title:
                print("{+} not find")
                continue

            warp_element = driver.find_element_by_css_selector(".ver-wrap")
            for li_element in warp_element.find_elements_by_tag_name("li"):
                if "APK" in li_element.text and "XAPK" not in li_element.text:
                    if "Variants" in li_element.text:
                        driver.get(li_element.find_element_by_tag_name("a").get_attribute("href"))
                        download_apk(driver.find_element_by_css_selector(".table-cell>a").get_attribute('href'))
                        # os.remove(os.path.join(get_stored_dir(), file))
                        break
                    else:
                        download_apk(li_element.find_element_by_tag_name("a").get_attribute("href"))
                        # os.remove(os.path.join(get_stored_dir(), file))
                        break
    driver.quit()
