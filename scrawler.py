#Date: 2017.12.30
#Writen By: QuanLongJie
#Function: download web pages
import re
import os
import requests

class page:
    ERROR_OK = 0
    ERROR_INPUT = 1
    ERROR_SERVER = 2
    ERROR_EXCEPT = 3
    ERROR_OTHER = 4
    def __init__(self, url, content, status_code):
        self.url = url
        self.content = content
        self.status  = status_code

    #parse pagecontent into title, head and body
    def parse(self):
        content = {'title' : '', 'head' : '', 'body' : ''}
        matchs = re.findall(r'<head.*</head>', self.content, re.DOTALL)
        if matchs[0] != None:
            content['head'] = matchs[0]
        matchs = re.findall(r'<title.*</title>', content['head'], re.DOTALL)
        if matchs[0] != None:
            content['title'] = matchs[0]
        matchs = re.findall(r'<body.*</body>', self.content, re.DOTALL)
        if matchs[0] != None:
            content['body'] = matchs[0]
        return content

#download page
def download(url, retry_times = 2):
    if url == None:
        return page(url, "", 1)
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return page(url, request.text, 0)
        if 500 <= request.status_code < 600:
            if retry_times == 0:
                return page(url, "", 2)
            else:
                return download(url, retry_times - 1)
    except:
        return page(url, "", 3)
    return page(url, "", 4)

#save page
def save(dir, filename, page, encoding = 'utf-8'):
    path = os.path.join(dir, filename)
    print(path)
    if os.path.exists(path):
        print('path exist')
        return
    else:
        print("not exit")
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = open(path, 'wb')
        #ignore wrong string
        content = page.content.encode(encoding, 'ignore')
        if file == None:
            return
        file.write(content)
        file.flush()
        file.close()





######below are test codes######
html = download("http://www.baidu.com")
if html.status == page.ERROR_EXCEPT:
    print("exception")
elif html.status == page.ERROR_INPUT:
    print("input none")
elif html.status == page.ERROR_SERVER:
    print("server error")
elif html.status == page.ERROR_OTHER:
    print("other error")
elif html.status == page.ERROR_OK:
    print("ok")


