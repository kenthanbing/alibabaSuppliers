import csv

# 新建一个data.csv文件，并且将数据保存到csv中
csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)
# 写入标题，采集企业名称，联系人，职位，座机，手机，传真，地址，邮编，国家，省份，城市，网址，阿里网址
writer.writerow(('company_name', 'contact_name', 'position', 'tel', 'mobile', 'fax', 'address', 'zip', 'country', 'province', 'city', 'website', 'ali_website'))

writer.writerow(('foo', 'bar'))
csvfile.close()