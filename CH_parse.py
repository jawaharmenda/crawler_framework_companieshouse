import json
import requests
import re
import os
from bs4 import BeautifulSoup

Path = r'/home/jawahar/chcrawl/output'
Path1 = r'/home/jawahar/chcrawl/ch_dump_json.txt'
Path2 = r'/home/jawahar/chcrawl/processed_ids.txt'

for filename in os.listdir(Path)[1825301:]:
    if not '_else' in filename or '_noemployments' in filename:
        with open(os.path.join(Path, filename)) as f , open(Path1,'a') as f1 , open(Path2,'a') as f2:
            print ("file processing :",filename)
            fullname=os.path.splitext(filename)[0]
            soup=BeautifulSoup(f, 'lxml')
            s1=soup.find_all('div',{'class':re.compile("appointment-")})
            f2.write(filename)
            f2.write("\n")
            f2.flush()
            for i in range(len(s1)):
                d = {}
                d['key']=filename
                try:
                    d['emp_id']=s1[i].find('a')['href']
                except:
                    d['emp_id']=None
                try:
                    d['name']=s1[i].find('span',{'id':'officer-name-{}'.format(i+1)}).text
                except:
                    d['name']=None
                try:
                    d['address']=s1[i].find('dd',{'class':'data'}).text
                except:
                    d['address']=None
                try:
                    d['status']=s1[i].find('span',{'id':'officer-status-tag-{}'.format(i+1)}).text
                except:
                    d['status']=None
                try:
                    d['role']=s1[i].find('dd',{'id':'officer-role-{}'.format(i+1)}).text
                except:
                    d['role']=None
                try:
                    d['dob']=s1[i].find('dd',{'id':'officer-date-of-birth-{}'.format(i+1)}).text
                except:
                    d['dob']=None
                try:
                    d['appointment_date']=s1[i].find('dd',{'id':'officer-appointed-on-{}'.format(i+1)}).text
                except:
                    d['appointment_date']=None
                try:
                    d['resignation_date']=s1[i].find('dd',{'id':'officer-resigned-on-{}'.format(i+1)}).text
                except:
                    d['resignation_date']=None
                try:
                    d['nationality']=s1[i].find('dd',{'id':'officer-nationality-{}'.format(i+1)}).text
                except:
                    d['nationality']=None
                try:
                    d['residence_country']=s1[i].find('dd',{'id':'officer-country-of-residence-{}'.format(i+1)}).text
                except:
                    d['residence_country']=None
                try:
                    d['occupation']=s1[i].find('dd',{'id':'officer-occupation-{}'.format(i+1)}).text
                except:
                    d['occupation']=None
                j = json.dumps(d)
                f1.write(j)
                f1.write("\n")
                f1.flush()
            f1.close()
            f2.close()
            f.close()