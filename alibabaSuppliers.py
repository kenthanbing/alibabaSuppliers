#! /usr/bin/env python
# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import csv
import re

# 打开一个火狐浏览器
driver = webdriver.Firefox()

# 登录的URL
login_url = 'https://passport.alibaba.com/icbu_login.htm'

# 跳转到登录页面
driver.get(login_url)

# 等待5秒，防止网速较差打不开页面就进行其他操作
time.sleep(2)

# 输入登录账号密码
driver.find_element_by_name('loginId').send_keys(input('Please enter your ID: '))
driver.find_element_by_name('password').send_keys(input('Please enter your password: '))
driver.find_element_by_name('submit-btn').send_keys(Keys.ENTER)
time.sleep(2)

# 跳转到搜索结果页面
section = input('Please enter section ID number: ')
search_result_url = f'https://www.alibaba.com/trade/search?&indexArea=company_en&category={section}&page=1'
driver.get(search_result_url)
time.sleep(2)

# 新建一个data.csv文件，并且将数据保存到csv中
csvfile = open(f'{section}.csv', 'w', encoding='utf8', newline='')
writer = csv.writer(csvfile)
# 写入标题，采集企业名称，联系人，职位，座机，手机，传真，地址，邮编，国家，省份，城市，网址，阿里网址
writer.writerow(('company_name', 'contact_name', 'position', 'tel', 'mobile', 'fax', 'address', 'zip_code', 'country', 'province', 'city', 'website', 'ali_website'))


# 找出搜索结果页数
last_page = int(driver.find_element_by_xpath("//div[@class='ui2-pagination-pages']/a[last()-1]").text)

# 循环翻页
for i in range(1,last_page+1):
    search_result_url = f'https://www.alibaba.com/trade/search?&indexArea=company_en&category={section}&page={i}'
    driver.get(search_result_url)
    time.sleep(2)
    company_list = [i.get_attribute('href') for i in driver.find_elements_by_link_text('Contact Details')]
    # 循环打开某页搜索结果每家公司页面
    for company in company_list:
        # 打开contacts页
        driver.get(company)
        time.sleep(2)
        # 爬取数据
        try:
            driver.find_element_by_link_text("View details").click()
            time.sleep(2)
        except:
            pass
        try:
            company_name = driver.find_element_by_xpath('//table[@class="contact-table"]/tr/td').text
        except:
            company_name = ''

        try:
            contact_name = driver.find_element_by_xpath('//div[@class="contact-name"]').text
        except:
            contact_name = ''

        try:
            position = driver.find_element_by_xpath('//div[@class="contact-job"]').text
        except:
            position = ''

        try:
            tel = driver.find_element_by_xpath("//th[text()='Telephone:']/following-sibling::td").text
        except:
            tel = ''

        try:
            mobile = driver.find_element_by_xpath("//th[text()='Mobile Phone:']/following-sibling::td").text
        except:
            mobile = ''

        try:
            fax = driver.find_element_by_xpath("//th[text()='Fax:']/following-sibling::td").text
        except:
            fax = ''

        try:
            address = driver.find_element_by_xpath("//th[text()='Address:']/following-sibling::td").text
        except:
            address = ''

        try:
            zip_code = driver.find_element_by_xpath("//th[text()='Zip:']/following-sibling::td").text
        except:
            zip_code = ''

        try:
            country = driver.find_element_by_xpath("//th[text()='Country/Region:']/following-sibling::td").text
        except:
            country = ''

        try:
            province = driver.find_element_by_xpath("//th[text()='Province/State:']/following-sibling::td").text
        except:
            province = ''

        try:
            city = driver.find_element_by_xpath("//th[text()='City:']/following-sibling::td").text
        except:
            city = ''

        try:
            website = driver.find_element_by_xpath('//table[@class="contact-table"]/tr[3]/td/div').text
        except:
            website = ''

        try:
            ali_website = driver.find_element_by_xpath('//table[@class="contact-table"]/tr[4]/td/a').text
        except:
            ali_website = ''

        data = (company_name, contact_name, position, tel, mobile, fax, address, zip_code, country, province, city, website, ali_website)
        writer.writerow(data)

# 关闭csv
csvfile.close()
# 关闭模拟浏览器
driver.close()


