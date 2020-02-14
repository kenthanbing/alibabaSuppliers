import re
company = 'http://tigerpet.en.alibaba.com/company_profile.html?spm=a2700.supplier-normal.35.3.65eb1cffcwJlHP#top-nav-bar'

pat = re.compile(r'.*?\.alibaba\.com/')
company_domain = pat.search(company).group()
contacts_page = company_domain + 'contactinfo.html'

print(contacts_page)