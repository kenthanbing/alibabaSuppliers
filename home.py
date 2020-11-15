#! /usr/bin/env python
# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, datetime, csv, os
import urllib.request

# 打开一个火狐浏览器
driver = webdriver.Firefox(log_path=os.devnull)

# 登录的URL
login_url = 'https://passport.alibaba.com/icbu_login.htm'

# 跳转到登录页面
driver.get(login_url)
time.sleep(5)

# 输入登录账号密码
driver.find_element_by_name('loginId').send_keys('kenthanbing@gmail.com')
time.sleep(2)
driver.find_element_by_name('password').send_keys('891120zxh')
time.sleep(2)
driver.find_element_by_name('submit-btn').send_keys(Keys.ENTER)

# 输入国家代码
section = input('Enter the 2-letter country code: ')

# 新建一个csv文件和一个writer
csvfile = open(f'{section}.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(csvfile)
# 企业名称，联系人，座机，手机，国家，网址，阿里网址
writer.writerow(('company_name', 'contact_name', 'tel', 'mobile', 'country', 'website', 'ali_website'))
    
# 跳转到搜索结果页面
search_result_url = f'https://www.alibaba.com/trade/search?keyword=home&country={section}&indexArea=company_en&page=1'
driver.get(search_result_url)

# 找出搜索结果页数
try:
    last_pagenumber_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, 
            "//div[@class='ui2-pagination-pages']/a[last()-1]")))
    last_pagenumber_str = last_pagenumber_element.text
    last_page = int(last_pagenumber_str)
except:
    last_pagenumber_str = '1'
    last_page = 1

# 打印总页数，开始时间，预计完成时间
print(section)
print('Total Pages: ' + last_pagenumber_str)

project_start_time = datetime.datetime.now()
print('Start Time: ' + project_start_time.strftime('%H:%M'))

seconds_cost = datetime.timedelta(seconds=270 * last_page)
project_finish_time = project_start_time + seconds_cost
print('Estimated Finish Time: ' + project_finish_time.strftime('%H:%M'))

# 循环翻页
for i in range(1,last_page+1):
    print(f'Page {i}')
    time_start=time.time()
    search_result_url = f'https://www.alibaba.com/trade/search?keyword=home&country={section}&indexArea=company_en&page={i}'
    driver.get(search_result_url)
    time.sleep(5)
    company_list = [i.get_attribute('href') for i in 
        driver.find_elements_by_link_text('Contact Details')]
    # 循环打开某页搜索结果每家公司页面
    for company in company_list:
        try:
            # 打开contacts页
            driver.get(company)
            time.sleep(2)
            # 点击View details       
            driver.find_element_by_link_text('View details').click()
            time.sleep(2)
        except:
            pass
        # 如果公司页无效，就跳过进行下一个循环
        try:
            company_name = driver.find_element_by_xpath('//table[@class="contact-table"]/tr/td').text
        except:
            continue

        try:
            contact_name = driver.find_element_by_xpath('//div[@class="contact-name"]').text
        except:
            contact_name = ''

        try:
            tel = driver.find_element_by_xpath(
                "//th[text()='Telephone:']/following-sibling::td"
                ).text
        except:
            tel = ''

        try:
            mobile = driver.find_element_by_xpath(
                "//th[text()='Mobile Phone:']/following-sibling::td"
                ).text
        except:
            mobile = ''    

        try:
            country = driver.find_element_by_xpath(
                "//th[text()='Country/Region:']/following-sibling::td"
                ).text
        except:
            country = ''

        try:
            website = driver.find_element_by_xpath(
                '//table[@class="contact-table"]/tr[3]/td/div'
                ).text
        except:
            website = ''

        try:
            ali_website = company
        except:
            ali_website = ''
            
        data = (company_name, contact_name, tel + '\t', mobile + '\t', country, website, ali_website)
        writer.writerow(data)

    time_end=time.time()
    print('Seconds Cost: ', time_end-time_start)

# 关闭csv
csvfile.close()
time.sleep(1)    

# 关闭模拟浏览器
driver.close()
time.sleep(1)