# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, os, openpyxl

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
Options().add_argument("log-level=3")

wb = openpyxl.load_workbook('database.xlsx')
sheet = wb['Sheet1']
i = 0
driver = webdriver.Chrome()
driver.get('https://news.sina.com.cn/roll/#pageid=153&lid=2515&etime=1684771200&stime=1684857600&ctime=1684857600&date=2023-05-23&k=&num=50&page=1')
for p in range(1, 20000):
    i += 1
    a = _news.find_element(By.CLASS_NAME, 'c_tit')
    name = a.find_element(By.XPATH, './a')
    href = name.get_attribute('href')
    time_ = _news.find_element(By.CLASS_NAME, 'c_time').text
    sheet.cell(i, 2).value = href
    subdriver = webdriver.Chrome()
    subdriver.get(href)
    try: 
        body = driver.find_element(By.CLASS_NAME, 'article')
        print(body.text)
        sheet.cell(i, 5).value = body.text
    except:
        pass
    try:
        editor = body.find_element(By.PARTIAL_LINK_TEXT, '责任编辑').text.lstrip('责任编辑：')
        sheet.cell(i, 4).value = editor
        print(editor)
    except:
        pass
    try:
        kw = driver.find_element(By.CLASS_NAME, 'keywords')
        print(kw.text)
    except:
        pass
    subdriver.close()

    for j in range(page_num):
        driver.find_element(By.PARTIAL_LINK_TEXT, '下一页').click()
        _news_list = driver.find_elements(By.XPATH, '//*[@id="d_list"]/ul/li')
        news_list = driver.find_elements(By.CLASS_NAME, 'c_tit')
        for _news in _news_list:
            a = _news.find_element(By.CLASS_NAME, 'c_tit')
            name = a.find_element(By.XPATH, './a')
            href = name.get_attribute('href')
            time_ = _news.find_element(By.CLASS_NAME, 'c_time').text
            sheet.cell(i, 2).value = href
            subdriver = webdriver.Chrome()
            subdriver.get(href)
            time.sleep(3)
            try: 
                body = driver.find_element(By.CLASS_NAME, 'article')
                print(body.text)
                sheet.cell(i, 5).value = body.text
            except:
                pass
            try:
                editor = body.find_element(By.PARTIAL_LINK_TEXT, '责任编辑').text.lstrip('责任编辑：')
                sheet.cell(i, 4).value = editor
                print(editor)
            except:
                pass
            try:
                kw = driver.find_element(By.CLASS_NAME, 'keywords')
                print(kw.text)
            except:
                pass

driver.close()
wb.close()
