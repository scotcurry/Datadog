from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://ubuntu-desktop.curryware.org:8088/')
title = driver.title

