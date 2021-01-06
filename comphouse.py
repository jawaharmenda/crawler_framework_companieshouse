import json
import requests
import io
import sys
import re
import os

import multiprocessing

from multiprocessing import Pool

from bs4 import BeautifulSoup
from random import choice
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
from lxml.html import fromstring

filename=sys.argv[1]
outputfilename=sys.argv[2]

def writetexttofile(text):
    print("appending text "+text+" to file")
    with open(outputfilename, "a") as text_file:
        text_file.write(text)
        text_file.write("\n")

def readurls():
    with open(filename, 'r') as f:
        x = f.read().splitlines()
    return x

#read all urls into a list
urllist=readurls()

def savefile(filename,text):
    print("saving file "+filename)
    with open(filename,'w') as f:
        f.write(text)

def read_proxy_list(dirpath):
    with open(dirpath, 'r') as f:
        x = f.read().splitlines()
    return x

proxies=set()
not_working_proxies_set=set()

def get_proxies4():
    print("connecting to proxy list 4 all")
    url="https://www.proxylist4all.com/wp-admin/admin-ajax.php?action=getProxyList&request=Elite"
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"}
    response = requests.get(url,headers=headers)

    jsonresp=json.loads(response.text)
    #print len(jsonresp)
    global proxies
    for i in range(0,len(jsonresp)):
        if(jsonresp[i]['type']=="Elite"):
            ip=jsonresp[i]['host']
            port=jsonresp[i]['port']
            proxy=str(ip)+":"+str(port)
            #print "proxy is "+str(ip)+":"+str(port)
            proxies.add(proxy)

def get_proxies3():
    print("connecting to proxy eliteproxy dot net")
    url='https://eliteproxy.net/elite-proxy/'
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"}
    response = requests.get(url,headers=headers)
    parser = fromstring(response.text)
    global proxies
    x=parser.xpath('//table[@class="blueTable"]//tr')
    for i in range(1,53):
        if (x[i].xpath('./td')[0].text != None):
            ip=x[i].xpath('./td')[0].text
            port=x[i].xpath('./td')[1].text
            proxy=ip+":"+port
            #print proxy
            proxies.add(proxy)

def get_proxies2():
    print("connecting to proxy id cloak")
    url='http://www.idcloak.com/proxylist/elite-proxy-list.html'
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"}
    response = requests.get(url,headers=headers)
    parser = fromstring(response.text)
    global proxies
    x=parser.xpath('//table[@id="sort"]//tr')
    for i in range(1,len(x)):
        ip=str(parser.xpath('//table[@id="sort"]/tr')[i].xpath('./td[8]/text()')[0])
        port=str(parser.xpath('//table[@id="sort"]/tr')[i].xpath('./td[7]/text()')[0])
        proxy=ip+":"+port
        proxies.add(proxy)

def get_proxies1():
    print("connecting to proxy ssl proxies")
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    global proxies
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            if i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            #Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)

def get_proxies():
    print("connecting to proxy")
    url1="https://www.proxy-list.download/api/v1/get?type=https&anon=elite"
    response=requests.get(url1)
    content=response.text
    savefile('proxylist',content)
    list=read_proxy_list("proxylist")
    global proxies
    proxies.update(list)


get_proxies1()
get_proxies()
#get_proxies3()
#get_proxies4()



userAgentList=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
"Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 YaBrowser/19.1.0.2644 Yowser/2.5 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 YaBrowser/19.1.1.909 Yowser/2.5 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
"Mozilla/5.0 (iPad; CPU OS 12_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.65",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Windows NT 6.1; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
"Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.68",
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
"Mozilla/5.0 (X11; CrOS x86_64 11151.113.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.127 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0"]

#headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8","Cache-Control":"max-age=0","host":"suite.endole.co.uk","Upgrade-Insecure-Requests":"1","user-agent":str(choice(userAgentList))}

#headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9","Pragma":"no-cache","Cache-Control":"no-cache","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8","Upgrade-Insecure-Requests":"1","DNT":"1","User-Agent":str(choice(userAgentList))}

headers={"User-Agent":str(choice(userAgentList))}

def worker(numberlist):
    missed_url_list=[]
    failed_proxy_list=[]

    proxylen=len(proxies)
    print("list length is "+str(len(proxies)))
    if(len(proxies)< 1):
        print("exhausted proxylist.Exiting")
        #os._exit(0)
    else:
        proxydns=str(choice(tuple(proxies)))

        print("proxy used is "+proxydns)
        proxy={"https":"https://"+proxydns,"http":"http://"+proxydns}


        url="https://find-and-update.company-information.service.gov.uk/company/%s/officers" %str(numberlist)
        savedfilename=str(numberlist)
        print("acessing url "+url)
        if(os.path.isfile(outputfilename+savedfilename) or os.path.isfile(outputfilename+savedfilename+"_else") or os.path.isfile(outputfilename+savedfilename+"_morepages") or os.path.isfile(outputfilename+savedfilename+"_noemployments")):
                #don't recrawl if crawled already .can happen if script got killed for some reason
            print("found filename in destination.Ignoring crawl for "+url)
        else:
            try:

                r=requests.get(url ,proxies=proxy,headers=headers, timeout=30,allow_redirects=True)
                

                if("pager" in r.text):
                    print("found good page")
                    savefile(outputfilename+savedfilename+"_morepages",r.text)
                elif("Role" in r.text):
                    print("found employments")
                    savefile(outputfilename+savedfilename,r.text)
                    #proxies.remove(proxydns)
                elif ("Sorry to stop you" in r.text):
                    print("challenge page found")
                    missed_url_list.append(numberlist)
                    #failed_proxy_list.append(proxydns)
                    proxies.remove(proxydns)
                    #best_proxies.add(proxydns)
                elif ("" in r.text):
                    print("got empty response..")
                    savefile(outputfilename+savedfilename+"_else",r.text)
                else:
                    print("Found no employments")
                    savefile(outputfilename+savedfilename+"_noemployments",r.text)

            except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError,Exception):
                print("got proxy error for "+proxydns)
                proxies.remove(proxydns)
                missed_url_list.append(numberlist)
                failed_proxy_list.append(proxydns)

    return missed_url_list,failed_proxy_list


processes=300




while(len(urllist) > 0):
    print("Total urls to crawl are "+str(len(urllist)))
    if(len(proxies) < 1):
        print("proxies length is "+str(len(proxies)))
        get_proxies1()
        #get_proxies()

    p=Pool(int(processes))
    result,not_working_list=zip(*p.map(worker,urllist))
    p.close()

    not_working_list=[ent for sublist in not_working_list for ent in sublist]
    not_working_proxies_set=set(not_working_list)
    proxies1=proxies-not_working_proxies_set
    proxies=proxies1

    missed_url_list=[ent for sublist in result for ent in sublist]
    missed_url_set=set(missed_url_list)
    print("missed url set len is "+str(len(missed_url_set)))
    urllist=missed_url_set
    #print(urllist)
    print(missed_url_set)
    print("Pending urls to crawl are "+str(len(urllist)))
print("done")
