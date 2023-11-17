import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def run_selenium_script(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    options = ChromeOptions()
    options.add_argument('--headless')
    chrome_driver_path = '/usr/local/bin/chromedriver'
    service = ChromeService(port=8088, executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    for counter in range(0, 26):

        print('Counter is: ' + str(counter))
        driver.get('http://ubuntu-desktop.curryware.org:8088')
        print(driver.title)

        wait_time = round(random.random(), 2)
        driver.implicitly_wait(wait_time)
        driver.get('http://ubuntu-desktop.curryware.org:8088/database_functions')
        print(driver.title)

        wait_time = round(random.random(), 2)
        driver.implicitly_wait(wait_time)
        driver.get('http://ubuntu-desktop.curryware.org:8088/chuckjoke')
        print(driver.title)

        wait_time = round(random.random(), 2)
        driver.implicitly_wait(wait_time)
        driver.get('http://ubuntu-desktop.curryware.org:8088/random_error')
        print(driver.title)

        force_error = random.randint(0, 99)
        if force_error < 5:
            print('Forcing an error')
            wait_time = round(random.random(), 2)
            driver.implicitly_wait(wait_time)
            driver.get('http://ubuntu-desktop.curryware.org:8088/forced_error')

        delay = round(random.random(), 2) * 10
        time.sleep(delay)

        wait_time = round(random.random(), 2)
        driver.implicitly_wait(wait_time)
        driver.get('http://ubuntu-desktop.curryware.org:8088/azure_container_app')
        print(driver.title)

    driver.close()


if __name__ == '__main__':
    run_selenium_script('Run Selenium')
