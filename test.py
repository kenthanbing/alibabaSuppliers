import json, time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 打开一个火狐浏览器
driver = webdriver.Firefox(service_log_path=os.devnull)

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

input('start: ')

json_in = open('KR.json', 'r')
json_out = open('KR_fixed.json', 'w')

kr_dict = json.load(json_in)

for company in kr_dict:
    if company['mobile'] == '8.21E+11' or company['mobile'].startswith('-'):
        url = company['ali_website']
        driver.get(url)
        time.sleep(2)
        # 点击View details       
        driver.find_element_by_link_text('View details').click()
        time.sleep(2)
        company['mobile'] = driver.find_element_by_xpath(
                "//th[text()='Mobile Phone:']/following-sibling::td"
                ).text

kr_str = json.dumps(kr_dict)
json_out.write(kr_str)

json_in.close()
json_out.close()

import re
company = 'http://tigerpet.en.alibaba.com/company_profile.html?spm=a2700.supplier-normal.35.3.65eb1cffcwJlHP#top-nav-bar'

pat = re.compile(r'.*?\.alibaba\.com/')
company_domain = pat.search(company).group()
contacts_page = company_domain + 'contactinfo.html'

print(contacts_page)
