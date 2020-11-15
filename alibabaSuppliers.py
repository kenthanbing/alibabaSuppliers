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

# 输入行业代码
sections_input = input('Enter the sections, seperated by ".": ')
sections = sections_input.split('.')

# 循环遍历行业代码
for section in sections:
    # 跳转到搜索结果页面，如需全球采集，去掉&country=CN
    search_result_url = f'https://www.alibaba.com/trade/search?&indexArea=company_en&category={section}&page=1&country=CN'
    driver.get(search_result_url)

    # 新建一个data.csv文件和一个writer
    csvfile = open(f'{section}.csv', 'w', encoding='utf8', newline='')
    writer = csv.writer(csvfile)
    # 企业名称，联系人，职位，座机，手机，传真，地址，邮编，国家，省份，城市，网址，阿里网址
    writer.writerow(('company_name', 'contact_name', 'position', 'tel', 'mobile',
        'fax', 'address', 'zip_code', 'country', 'province',
        'city', 'website', 'ali_website'))

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

    seconds_cost = datetime.timedelta(seconds=480 * last_page)
    project_finish_time = project_start_time + seconds_cost
    print('Estimated Finish Time: ' + project_finish_time.strftime('%H:%M'))

    # 循环翻页
    for i in range(1,last_page+1):
        print(f'Page {i}')
        time_start=time.time()
        # 如需全球采集，去掉&country=CN
        search_result_url = f'https://www.alibaba.com/trade/search?&indexArea=company_en&country=CN&category={section}&page={i}'
        driver.get(search_result_url)
        time.sleep(5)
        company_list = [i.get_attribute('href') for i in 
            driver.find_elements_by_link_text('Contact Details')]
        # 循环打开某页搜索结果每家公司页面
        for company in company_list:
            try:
                # 打开contacts页
                driver.get(company)
                time.sleep(5)
                # 爬取数据        
                driver.find_element_by_link_text('View details').click()
                time.sleep(5)
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
                fax = driver.find_element_by_xpath("//th[text()='Fax:']/following-sibling::td").text
            except:
                fax = ''

            try:
                address = driver.find_element_by_xpath(
                    "//th[text()='Address:']/following-sibling::td"
                    ).text
            except:
                address = ''

            try:
                zip_code = driver.find_element_by_xpath("//th[text()='Zip:']/following-sibling::td").text
            except:
                zip_code = ''

            try:
                country = driver.find_element_by_xpath(
                    "//th[text()='Country/Region:']/following-sibling::td"
                    ).text
            except:
                country = ''

            try:
                province = driver.find_element_by_xpath(
                    "//th[text()='Province/State:']/following-sibling::td"
                    ).text
            except:
                province = ''

            try:
                city = driver.find_element_by_xpath("//th[text()='City:']/following-sibling::td").text
            except:
                city = ''

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

            data = (company_name, contact_name, position, tel + '\t', mobile + '\t', fax + '\t', address, zip_code + '\t', 
                country, province, city, website, ali_website)
            writer.writerow(data)

        time_end=time.time()
        print('Seconds Cost: ', time_end-time_start)

    # 关闭csv
    csvfile.close()
    time.sleep(1)

# 关闭模拟浏览器
driver.close()
time.sleep(1)